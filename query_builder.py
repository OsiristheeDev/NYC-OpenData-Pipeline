from keywords import micro_mobility,collision_persons_table_col,collision_location_table_col
import re
import datetime as dt

#Joins the list of mobility devices into one string for the SOQL query
micro_mobility_combined = "', '".join(micro_mobility)

persons_table_columns_joined = ','.join(collision_persons_table_col)

location_table_columns_joined = ','.join(collision_location_table_col)

combined_collision_persons_columns = ", ".join([f":{c}" for c in collision_persons_table_col])

combined_collision_location_columns =", ".join([f":{c}" for c in collision_location_table_col])

combined_collision_persons_variables = ", ".join(f"{c} = EXCLUDED.{c}" for c in collision_persons_table_col if c[-2:] != "id")

combined_collision_location_variables =", ".join(f"{c} = EXCLUDED.{c}" for c in collision_location_table_col if c[-2:] != "id")

vehicles_query = f"""SELECT *
                        WHERE vehicle_type_code1 IN ('{micro_mobility_combined}')  OR
                              vehicle_type_code2 IN ('{micro_mobility_combined}')  OR
                              vehicle_type_code_3 IN ('{micro_mobility_combined}')  OR 
                              vehicle_type_code_4 IN ('{micro_mobility_combined}')  OR 
                              vehicle_type_code_5 IN ('{micro_mobility_combined}')
                        LIMIT 1000000"""

collisions_persons_upsert_query = f"""INSERT INTO nyc.collisions_persons ({persons_table_columns_joined}) 
                        VALUES ({combined_collision_persons_columns}) 
                        ON CONFLICT (unique_id)  
                        DO UPDATE SET 
                        {combined_collision_persons_variables};"""

collisions_locations_upsert_query = f"""INSERT INTO nyc.collisions_locations ({location_table_columns_joined})
                        VALUES ({combined_collision_location_columns}) 
                        ON CONFLICT (collision_id)  
                        DO UPDATE SET 
                        {combined_collision_location_variables};"""

def revise_vehicle_query(last_run_date: dt.datetime,today_date: dt.datetime) -> str:
   last_run_date = last_run_date.isoformat()
   today_date = today_date.isoformat()
   update_logic = f":updated_at BETWEEN '{last_run_date}' AND '{today_date}'"
   updated_vehicle_query = re.sub(r'\)\s\s',f') AND {update_logic} ',vehicles_query)
   return updated_vehicle_query