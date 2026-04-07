from dotenv import load_dotenv
import os
import pandas as pd 
from sodapy import Socrata
from keywords import micro_mobility 
from pathlib import Path
import datetime

load_dotenv()

working_directory = Path.cwd()
data_directory = Path(working_directory/'data') 
today_date = datetime.date.today()

NYC_APP_TOKEN = os.getenv('NYC_APP_TOKEN')

client = Socrata("data.cityofnewyork.us",NYC_APP_TOKEN)

#Joins the list of mobility devices into one string for SOQL
micro_mobility_combined = "', '".join(micro_mobility)

#Checks the NYC Motor Vehicle Collision for all crashes involving mobility devices 
results = client.get("h9gi-nx95",
                     query=f"""SELECT * 
                     WHERE vehicle_type_code2 IN ('{micro_mobility_combined}') OR
                           vehicle_type_code_3 IN ('{micro_mobility_combined}') OR 
                           vehicle_type_code_4 IN ('{micro_mobility_combined}') OR 
                           vehicle_type_code_5 IN ('{micro_mobility_combined}')
                     LIMIT 1000000""")

df = pd.DataFrame.from_records(results)

df = df.sort_values(by='crash_date',ascending=False)

df.to_csv(data_directory/f'nyc_collisions_{today_date}.csv',index=False)
