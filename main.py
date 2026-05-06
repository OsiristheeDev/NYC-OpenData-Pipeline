import sys
import pandas as pd 
from pathlib import Path
import datetime as dt
from sqlalchemy import create_engine,text
from dotenv import load_dotenv
from sodapy import Socrata
import os
from extract_data import extract_opendata,extract_persons_init
from transform_data import rename_columns,create_crash_datetime_column,consolidate_values, change_col_dtype
from query_builder import collisions_persons_upsert_query,collisions_locations_upsert_query,revise_vehicle_query,vehicles_query
from numpy import array_split
from keywords import collision_api_request_fields,table_names
import numpy as np
import logging 

load_dotenv()

working_directory = Path.cwd()
data_directory = Path(working_directory/'data') 
sql_directory = Path(working_directory/'SQL')
today_date = dt.datetime.now().replace(microsecond=0)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

f_handler = logging.FileHandler(working_directory/'pipe.log')
f_handler.setLevel(logging.WARNING)

s_handler = logging.StreamHandler()
s_handler.setLevel(logging.INFO)

logger.addHandler(f_handler)
logger.addHandler(s_handler)

SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_USERNAME = os.getenv('SERVER_USERNAME')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
SERVER_NAME = os.getenv('SERVER_NAME')

NYC_APP_TOKEN = os.getenv('NYC_APP_TOKEN')
NYC_OPEN_DATA_URL = "data.cityofnewyork.us"

all_tables_exist= False

new_col_names = {'vehicle_type_code1': 'vehicle_type_code_1',
              'vehicle_type_code2': 'vehicle_type_code_2'}

persons_dtype = {'person_age':'Int16',
             'vehicle_id':'Int64'}

nyc_vehicles_dataset = 'h9gi-nx95'
nyc_persons_dataset = 'f55k-p6yu'

def init_client(opendata_url:str = NYC_OPEN_DATA_URL,app_token:str = NYC_APP_TOKEN) -> Socrata: 
      """Initialize the Socrata object used to access the dataset of choice 
      Defaults to NYC Open Data"""
      client = Socrata(opendata_url,app_token)

      #Confirm the app token and URL is valid before proceeding
      try:
        test_results = client.get(nyc_vehicles_dataset,limit=1)
      except Exception:
        logger.exception('Unable to initialize client. is the url correct? Is your app_token valid?')
        sys.exit()

      return client

def log_dataframe_info(df:pd.DataFrame,datetime_column:str = 'crash_datetime') -> str:
    "Assesses a dataframe and writes essential metrics obtained to a file"
    sorted_s = df[datetime_column].sort_values(ascending=False)

    num_of_records = len(df)
    recent_record = sorted_s.iloc[0]
    earliest_record = sorted_s.iloc[-1]

    report_string = f"""This process ran {today_date}
    This dataframe has a total of {num_of_records}
                        The most recent being {recent_record}
                        the earliest record being {earliest_record}\n"""
    
    return report_string

def create_tables(engine: object):
    '''Creates the tables necessary for the pipeline to run in the SQL database'''
    with open(sql_directory/'init.SQL','r') as sql_file:
        contents = sql_file.read()
        list_ofqueries = [q for q in contents.split(';') if q.strip()]

    with engine.begin() as connection:
        for query in list_ofqueries:
            try:
                connection.execute(text(query))
            except Exception:
                logger.exception('Unable to create tables')

def verify_tables_exist(table_names:list,engine: object) -> bool:
    with engine.connect() as connection:
        for table in table_names:
            try:
                t_exists = connection.execute(text(F"SELECT to_regclass('{table}') IS NOT NULL")).one()[0]
            except Exception:
                logger.exception('Something went wrong during tables verification. Are your table names correct?')
                return False
            
            if not t_exists:
                return False
        
        return True


def main():
    logger.info("Before we begin let's confirm the Server is online")
    
    engine = create_engine(f"postgresql://{SERVER_USERNAME}:{SERVER_PASSWORD}@{SERVER_HOST}/{SERVER_NAME}")

    if verify_tables_exist(table_names,engine): 
        logger.info('ALL THE TABLES EXISTS')
        all_tables_exist = True
        first_run = False
    else:
        logger.info("One or all of the tables don't exist let's create them")
        create_tables(engine=engine)
        verify_tables_exist(table_names,engine)
        all_tables_exist = True
        first_run = True
        
    #Determine if the runtime table has entries already to determine if the query should be an update or initial run
    with engine.begin() as connection:
        server_result = connection.execute(text("""SELECT run_dates
                                                    FROM nyc.runtimes
                                                    ORDER BY run_dates DESC
                                                    LIMIT 1;"""))
        last_run_date = server_result.fetchone()
    if last_run_date != None:
        last_run_date = last_run_date[0]
    else:
        last_run_date = None

    if last_run_date == None:
        logger.info('The server has never run before so of course it needs an update')
        time_for_refresh = True
    elif today_date.date() > last_run_date.date():
        logger.info('The server is not up to date')
        time_for_refresh = True
    else:
        logger.info('The server is up to date ')
        time_for_refresh = False
        sys.exit()
        
    logger.info("Woohoo the server is online. Let's begin the extraction process")

    # - Initialize Socrata Client
    client = init_client(NYC_OPEN_DATA_URL,NYC_APP_TOKEN)
    
    #STEP ONE: EXTRACT Vehicle Records
    try:
        if time_for_refresh is True and all_tables_exist is True and first_run is False:
            logger.info("Updating existing tables")
            vehicles_query_update = revise_vehicle_query(last_run_date,today_date)

            logger.info('Now extracting vehicle/location data')
            vehicle_records = extract_opendata(client,
                                                nyc_vehicles_dataset,
                                                vehicles_query_update)

        elif time_for_refresh is True and all_tables_exist is True and first_run is True:
            vehicle_records = extract_opendata(client,
                                                nyc_vehicles_dataset,
                                                vehicles_query)
        else:
            logger.info("Server is up to date. No need for an update")
            sys.exit()

    except Exception:
        logger.exception("The Vehicle Api request was unsuccessful")
        sys.exit()

    veh_df = pd.DataFrame.from_records(vehicle_records,columns=collision_api_request_fields)
    
    #Data Quality Check 
    if len(veh_df) <= 1:
      logger.error("No collision IDs returned, something went wrong with the vehicle extract")
      sys.exit()
    else:
        veh_collision_ids = veh_df['collision_id'].to_list()

    #STEP TWO: EXTRACT Person Records
    logger.info('Now extracting person data')

    #If you try to pass a large number of collision_ids the API refuses the request so the request has to be split up
    if len(veh_collision_ids) > 5000:
        collision_id_chunks = array_split(veh_collision_ids,80)

        total_chunks = len(collision_id_chunks)

        try:
            persons_records = extract_persons_init(client,nyc_persons_dataset,
                                            total_chunks,collision_id_chunks)
        
        except Exception:
            logger.exception("The person api request was unsuccessful")
            sys.exit()
    else:
        combined_collision_ids = "','".join(veh_collision_ids)
        person_query = f"""SELECT *
                    WHERE collision_id IN ('{combined_collision_ids}')
                    LIMIT 1000000"""
        try:
            persons_records = extract_opendata(client,nyc_persons_dataset,person_query)
        except Exception:
            logger.exception("The person api request was unsuccessful. The amount of collision ids reviewed is likely too many")
            sys.exit()

    persons_df = pd.DataFrame.from_records(persons_records)

    #Data Quality Check
    if len(persons_df) <= 1:
      logger.error("No collision IDs returned, something went wrong with the person extract")
      sys.exit()

    #STEP THREE: Clean The Data
    try:
        veh_df = veh_df.pipe(rename_columns,new_col_map=new_col_names).pipe(create_crash_datetime_column).pipe(consolidate_values)
        veh_df = veh_df.replace({np.nan: None,pd.NaT: None,pd.NA: None})
        logger.info('Vehicle Dataframe successfully cleaned')
    except Exception:
        logger.exception("Unable to clean the vehicle dataframe")
        sys.exit()

    try:
        persons_df = persons_df.pipe(create_crash_datetime_column).pipe(change_col_dtype,col_dtype_map=persons_dtype)
        #NP.NaN and similar types cause issues when loading into SOQL must be converted
        persons_df = persons_df.replace({np.nan: None,pd.NaT: None,pd.NA: None})
        logger.info('Persons Dataframe successfully cleaned')
    except Exception:
        logger.exception("Unable to clean the persons dataframe")
        sys.exit()

    #Find which collision ids do not appear in the person dataset 
    person_ids = set(persons_df['collision_id'])
    missing_collision_ids = []

    for id in veh_collision_ids:
        if id not in person_ids:
            missing_collision_ids.append(id)
        
    #Creating a backup incase something goes wrong when uploading to the server
    with open(data_directory/f'nyc_collisions_backup_{today_date.date()}','w') as collisions_backup:
        veh_df.to_csv(collisions_backup,index=False)

    with open(data_directory/f'nyc_persons_backup_{today_date.date()}','w') as persons_backup:
        persons_df.to_csv(persons_backup,index=False)

    logger.info('Records successfully backed up')

    #STEP FOUR LOAD The data into the SQL Server
    with engine.begin() as connection:
        try:
            logger.info('Now loading vehicle records into the server')
            vehicle_records = veh_df.to_dict("records")
            connection.execute(text(collisions_locations_upsert_query),parameters=vehicle_records)
            logger.info('Now loading vehicle records into the server')
            persons_records = persons_df.to_dict("records")
            connection.execute(text(collisions_persons_upsert_query),parameters=persons_records)
            logger.info('The data has been successfully loaded into the server congratulations')
        except Exception:
            logger.exception('We were unable to upsert successfully to the tables')
            raise 
    
    #Step 5 Update runtimes with new date and time 
    total_new_records = len(veh_df) + len(persons_df)
    runtime_update_query = f"""INSERT INTO nyc.runtimes (run_dates,record_num)
                              VALUES ('{today_date}',{total_new_records})"""

    with engine.begin() as connection:
         connection.execute(text(runtime_update_query))
         logger.info('Runtimes successfully updated!')

    missing_ids_note = f"""{len(missing_collision_ids)} collision records do not have entries in the person dataset
                        The ids that are missing are {missing_collision_ids}\n"""
    
    #Writing Dataframe Metrics to a txt file to keep track of what's run and a log on it
    with open(data_directory/'collisions_nyc_run_log.txt','a') as collision_data:
        collision_data.write(log_dataframe_info(veh_df))
        
    with open(data_directory/'persons_nyc_run_log.txt','a') as person_data:
        person_metrics = log_dataframe_info(persons_df)
        person_data.write(person_metrics + missing_ids_note)

if __name__ == "__main__":
    main()
