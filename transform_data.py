import pandas as pd 
from keywords import vehicle_categories
import logging

logger = logging.getLogger(__name__)

def rename_columns(df:pd.DataFrame,new_col_map: dict) -> pd.DataFrame:
    "Renames a dataframe's columns by matching the old column to the new column name"
    df = df.rename(columns=new_col_map)
    for k,v in new_col_map.items():
          
          logger.info(f"column {k} has been renamed to {v}")

    return df

def create_crash_datetime_column(df:pd.DataFrame) -> pd.DataFrame:
     
    #Slices the date column to only include the date and not the time.
    df['crash_date'] = df['crash_date'].apply(lambda s: s[:10])

    #Combine the date and time category into 1 column then convert it to a datetime format 
    df['crash_datetime'] = df['crash_date']+ '-' + df['crash_time']
    df['crash_datetime'] = pd.to_datetime(df['crash_datetime'],format="%Y-%m-%d-%H:%M")

    df = df.drop(columns=['crash_date','crash_time'])

    return df

def consolidate_values(df:pd.DataFrame) -> pd.DataFrame:
    """Replaces the various vehicle names with a common unifier for each vehicle column
        EX: 'bike', 'Bicycle', 'BICYCLE' -> Becomes Bike. Review keywords for full matching"""
    
    #loops until 6 because there are 5 vehicle_code categories
    for i in range(1,6): 

        for replacement_val,og_val in vehicle_categories.items():
            df[f'vehicle_type_code_{i}'] = df[f'vehicle_type_code_{i}'].replace(og_val,replacement_val)
        

    return df


def change_col_dtype(df:pd.DataFrame,col_dtype_map:dict) -> pd.DataFrame:
    """Uses a dictionary to update a columns dtype
    EX: {'fraction':'float'} would change a df column with the name fraction to type float"""
    for col_name,dtype in col_dtype_map.items():
        df[col_name] = df[col_name].astype(dtype)

    return df
    
# - TESTS
"""
assert set(vehicle_categories.keys()).issubset(set(df['vehicle_type_code_1'].unique().tolist()))
assert len(df[df['collision_id'].isna()]) == 0, "One of your entries is missing its collision id"
"""

