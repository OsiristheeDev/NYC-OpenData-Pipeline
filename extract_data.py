from sodapy import Socrata
import random
import time
import logging

logger = logging.getLogger(__name__)

#Checks the NYC Motor Vehicle Collision for all crashes involving micro-mobility vehicles 
def extract_opendata(socrata_client:Socrata,dataset_identifier:str,sql_string:str) -> list[list]:
      """Using the previously initialized Socrata client query the dataset of choice with SQL to return a dataframe with those results"""
      results = socrata_client.get(dataset_identifier,
                        query=sql_string)

      return results

def extract_persons_init(socrata_client:Socrata,dataset_identifier:str,total_chunks:int, collision_id_chunks:list) -> list[list]:
    """Pulls person data from the Motor Vehicle dataset via chunks"""
    results_list = []

    for i in range(1,total_chunks+1):

        working_chunk = collision_id_chunks[i-1]
        #Converts the numbers in working_chunk to strings
        conv_working_chunk = [str(num) for num in working_chunk]
        #Concats to one string so it can be sent through the api
        conv_working_chunk_combined = ', '.join(conv_working_chunk)

        person_query = f"""SELECT *
                    WHERE collision_id IN ({conv_working_chunk_combined})
                    LIMIT 1000000"""
       
        results = extract_opendata(socrata_client,dataset_identifier,person_query)
        
        #To ensure api requests aren't made too quickly
        time.sleep(random.randint(1,5))
        
        results_list.extend(results)
        
        #Every 10 percent update progress
        if total_chunks > 5:
            if i % (round(total_chunks *0.1)) == 0:
                logger.info(f'Your api request is {(i / total_chunks) *100}% complete')
    
    return results_list