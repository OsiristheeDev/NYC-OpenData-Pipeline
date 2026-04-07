from dotenv import load_dotenv
import os
import pandas as pd 
from sodapy import Socrata
from keywords import micro_mobility 
from pathlib import Path
import datetime
import json
import numpy as np
import time
import random

load_dotenv()

NYC_APP_TOKEN = os.getenv('NYC_APP_TOKEN')

start_time = time.time()
working_directory = Path.cwd()
data_directory = Path(working_directory/'data') 
today_date = datetime.date.today()
file_date = "2026-03-27"

client = Socrata("data.cityofnewyork.us",NYC_APP_TOKEN)

with open(data_directory/f'collision_ids_{file_date}.json','r') as collision_file:
    contents = collision_file.read()
    collision_list = json.loads(contents)

collision_ids_chunks = np.array_split(collision_list,80)

total_chunks = len(collision_ids_chunks)

i=1
results_list = []

while i <= total_chunks:

    working_chunk = collision_ids_chunks[i-1]
    #Converts the numbers in working_chunk to strings
    conv_working_chunk = [str(num) for num in working_chunk]
    #Converts to one string so it can be sent through the api
    conv_working_chunk = ", ".join(conv_working_chunk)

    results = client.get('f55k-p6yu',
                        query=f"""SELECT *
                WHERE collision_id IN ({conv_working_chunk})
                LIMIT 1000000""")
    
    #To ensure I don't make too many api requests too quick
    time.sleep(random.randint(1,5))
    
    results_list.extend(results)
    i += 1

df = pd.DataFrame(results_list)


#Write the results to csv file 
df.to_csv(data_directory/f'nyc_persons_collisions_{file_date}.csv',index=False)
end_time = time.time()

print(f'Process complete total time {end_time-start_time}')
