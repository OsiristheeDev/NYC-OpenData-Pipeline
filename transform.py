import pandas as pd 
from pathlib import Path
import datetime as dt
from keywords import *
import json

working_directory = Path.cwd()
data_directory = Path(working_directory/'data') 
file_date = "2026-03-27"

pd.set_option('display.max_rows', None)

df = pd.read_csv(data_directory/f'nyc_collisions_{file_date}.csv')

new_col_names = {'vehicle_type_code1': 'vehicle_type_code_1',
              'vehicle_type_code2': 'vehicle_type_code_2'}

df = df.rename(columns=new_col_names)

#Slices the date column to only include the date and not the time.
df['crash_date'] = df['crash_date'].apply(lambda s: s[:10])

df['crash_date'] = pd.to_datetime(df['crash_date'])

#Converts the time column from string to date time
df['crash_time'] = pd.to_datetime(df['crash_time'],format='%H:%M').dt.strftime('%H:%M')
print(df['crash_time'].head())

"""Replaces the various vehicle names with a common unifier for each vehicle column
EX: 'Bike', 'Bicycle', 'BICYCLE' -> Becomes Bike"""
i=1
while i < 6: 
    for replacement_val,og_val in vehicle_categories.items():
        df[f'vehicle_type_code_{i}'] = df[f'vehicle_type_code_{i}'].replace(og_val,replacement_val)
    i += 1
    
# - TESTS
"""
assert set(vehicle_categories.keys()).issubset(set(df['vehicle_type_code_1'].unique().tolist()))
assert len(df[df['collision_id'].isna()]) == 0, "One of your entries is missing its collision id"
"""
print(df['collision_id'].head())
collision_ids = df['collision_id'].to_list()
'''
with open(data_directory/f"collision_ids_{file_date}.json","w") as collisions_file:
    contents = json.dumps(collision_ids)
    collisions_file.write(contents)
'''
