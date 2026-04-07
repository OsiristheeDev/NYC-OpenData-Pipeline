import pandas as pd 
from pathlib import Path
import datetime as dt
from keywords import *
from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_PASSWORD = os.getenv('SQL_PASSWORD')

working_directory = Path.cwd()
data_directory = Path(working_directory/'data') 
file_date = "2026-03-27"

pd.set_option('display.max_rows', None)

dtype_list = ['person_type', 'person_injury', 'ped_role', 'person_sex', 
              'ejection', 'emotional_status', 'bodily_injury', 'position_in_vehicle',
             'safety_equipment', 'complaint', 'ped_location', 'ped_action',
             'contributing_factor_1', 'contributing_factor_2']

dtype_dict = {l:'category' for l in dtype_list}

df = pd.read_csv(data_directory/f'nyc_persons_collisions_{file_date}.csv',low_memory=False)

df['crash_date'] = df['crash_date'].apply(lambda s: s[:10])

#Combine the date and time cateogry into 1 then converts it to a datetime format 
df['crash_datetime'] = df['crash_date']+ '-' + df['crash_time']
df['crash_datetime'] = pd.to_datetime(df['crash_datetime'],format="%Y-%m-%d-%H:%M")
df = df.drop(columns=['crash_date','crash_time'])
df['person_age'] = df['person_age'].astype('Int16')
df['vehicle_id'] = df['vehicle_id'].astype('Int64')

engine = create_engine(f'postgresql://Tajairi:{DATABASE_PASSWORD}@192.168.1.205/postgres')
engine.connect

df.to_sql('nyc_collisions_persons',con=engine)
print('The server is now live')

'''
This is to see how many unique entries are in each colum
for col in sample.columns:
    num_of_unique_entries = sample[col].nunique()
    pct =  (num_of_unique_entries / len(sample)) *100
    print(round(pct,2))

    if round(pct) <= 0.05:
        dtype_list.append(col)

print(dtype_list)
'''
