micro_mobility = [
    # E-bikes and bikes (existing)
    'e-bike', 'bike', 'BICYCLE', 'E-Bik','E BIK',
    'E-BIK', 'EBIKE', 'Ebike', 'E-bike', 'E-BIKE', 'E-bike', 
    'E bike', 'Citi bike','Electric B', 'electric s', 
    'e-bi', 'e bik', 'e-bike','Bike','BIKE','E-Bike',
    'Bicycle', 'BICYC', 'Bicyc', 'PEDAL BIKE',
    # Scooter variations (kick/push scooters and e-scooters)
    'e-scooter','E-SCOOTER','E-scooter', 'e-scooter','E scooter', 'E SCOOTER',
    'E Sco', 'e sco','E-Sco',
    'scooter', 'SCOOTER', 'Scooter',
    'scoot', 'Scoot', 'SCOOT',
    'scoo', 'SCOO', 'scooc', 'SCOOTOR',
    'kick scoot', 'PUSH SCOOT',
    'Razor Scoo', 'RAZOR SCOO',
    'Lime Scoot',
    'Electric S', 'ELECTRIC S',
    # Skateboard variations
    'skate', 'SKATE', 'skateboard', 'Skateboard', 'SKATEBOARD',
    'MOTOR SKAT','E-SKATEBOA', 'e skate bo',
    # Inline skates / Roller skates
    'In Line Sk',
    # Two-wheeled personal devices
    '2 wheel sc',
    # Unicycle variations
    'UNICYCLE', 'E-UNICYCLE',
    'ELEC. UNIC', 'Ele. Unicy',
    # Pedicabs (bike taxis)
    'pedicab', 'PEDICAB', 'Pedicab', 'pedic', 'PEDIC',
    # Other micro-mobility
    'HOVERBOARD',
    'one wheel', 'ONE WHEEL'
]

table_names =['nyc.collisions_persons','nyc.collisions_locations','nyc.runtimes']

injury_types = ['Eye', 'Elbow-Lower-Arm-Hand', 'Knee-Lower Leg Foot', 'Back', 
              'Hip-Upper Leg', 'Shoulder - Upper Arm', 'Unknown', 'Face',
                'Abdomen - Pelvis', 'Neck', 'Chest', 'Does Not Apply', 'Entire Body', 'Head']

complaints = ['Contusion - Bruise', 'Minor Burn', 'Amputation', 'Severe Burn', 
              'None Visible', 'Fracture - Dislocation', 'Fracture - Distorted - Dislocation', 
              'Severe Bleeding', 'Minor Bleeding', 'Internal', 'Whiplash', 'Crush Injuries', 
              'Unknown', 'Complaint of Pain or Nausea', 'Concussion', 'Does Not Apply', 
              'Severe Lacerations', 'Moderate Burn', 'Complaint of Pain', 'Abrasion', 'Paralysis']

emotional_status = ['Unknown', 'Semiconscious', 'Does Not Apply', 'Unconscious', 'Incoherent', 
                    'Apparent Death', 'Conscious', 'Shock']

collision_persons_table_col = ["unique_id","collision_id","person_id",         
            "person_type","person_injury","vehicle_id",          
            "ped_role", "person_sex", "person_age",           
            "ejection", "emotional_status",     
            "bodily_injury", "position_in_vehicle",  
            "safety_equipment", "complaint",            
            "ped_location", "ped_action",           
            "contributing_factor_1",               
            "contributing_factor_2","crash_datetime"]

collision_location_table_col = [
    "crash_datetime",
    "borough",
    "zip_code",
    "latitude",
    "longitude",
    "on_street_name",
    "off_street_name",
    "number_of_persons_injured",
    "number_of_persons_killed",
    "number_of_pedestrians_injured",
    "number_of_pedestrians_killed",
    "number_of_cyclist_injured",
    "number_of_cyclist_killed",
    "number_of_motorist_injured",
    "number_of_motorist_killed",
    "contributing_factor_vehicle_1",
    "contributing_factor_vehicle_2",
    "contributing_factor_vehicle_3",
    "contributing_factor_vehicle_4",
    "contributing_factor_vehicle_5",
    "vehicle_type_code_1",
    "vehicle_type_code_2",
    "vehicle_type_code_3",
    "vehicle_type_code_4",
    "vehicle_type_code_5",
    "cross_street_name",
    "collision_id" 
]
collision_api_request_fields = [
    "crash_date",
    "crash_time",
    "borough",
    "zip_code",
    "latitude",
    "longitude",
    "on_street_name",
    "off_street_name",
    "number_of_persons_injured",
    "number_of_persons_killed",
    "number_of_pedestrians_injured",
    "number_of_pedestrians_killed",
    "number_of_cyclist_injured",
    "number_of_cyclist_killed",
    "number_of_motorist_injured",
    "number_of_motorist_killed",
    "contributing_factor_vehicle_1",
    "contributing_factor_vehicle_2",
    "contributing_factor_vehicle_3",
    "contributing_factor_vehicle_4",
    "contributing_factor_vehicle_5",
    "vehicle_type_code1",
    "vehicle_type_code2",
    "vehicle_type_code_3",
    "vehicle_type_code_4",
    "vehicle_type_code_5",
    "cross_street_name",
    "collision_id" 
]


vehicle_categories = {
 
    # NYC Vehicle categories
    # =================
 
    "Sedan": ['4 dr sedan', '2 dr sedan', 'SEDAN', 'PASSENGER', 'PASSENGER VEHICLE',
        
        'PAS', 'Convertible', '3-Door', 'LIVERY VEHICLE',
        'LIMO', 'LIMOU','TAXI', 'Taxi', 'YELLOW TAX', 'YELLO', 'FOR HIRE VEHICLE',
    ],
 
    "SUV": [
        'Station Wagon/Sport Utility Vehicle', 'SPORT UTILITY / STATION WAGON',
        'SUV', 'SUBN/Van', 'Surburban', 'SEDONA', 'White subu',
    ],
    "Pick Up Truck": [
        'Pick-up Truck', 'PICK-UP TRUCK', 'Pick up Truck', 'Pick up tr', 'PICK-UP TR', 'PICK UP TR',
        'PICK UP', 'pickup', 'PKUP', 'PK', 'DODGE RAM','Pickup with mounted Camper',
    ],
    "Van": [
        'Van', 'van', 'VAN', 'Work Van',
        'Panel Van', 'FORD TRANS', 'Ford sprin', 'SPRINTER V',
        'Refrigerated Van', 'VAN TRUCK', 'FREIGT VAN', 'Van Camper','AMBULETTE',
    ],
 
    "Heavy Commercial - Light": [
        # medium-duty: cargo vans at upper end, smaller box trucks, delivery vehicles
        'Box Truck', 'Box truck', 'box t', 'BOX', 'DELIVERY T', 'COM DELIVE',
        'DELV WH', 'delv', 'DELIV', 'Utility', 'UTILITY', 'Commercial', 'COM',
        'COMME', 'SMALL COM VEH(4 TIRES) ', 'Chassis Cab', 'Open Body',
        'Stake or Rack', 'Flat Bed', 'FLAT BED T', 'Flat Rack', 'Glass Rack',
        'Beverage Truck', 'BTM', 'Armored Truck', 'SELF INSUR', 'SELF','Landscapin',
        'Tow Truck', 'Tow Truck / Wrecker', 'tow-truck', 'TOW TRUCK', 'Tow truck','Motorized Home'
    ],
 
    "Heavy Commercial - Medium": [
        # heavy medium-duty: larger box trucks, specialty commercial
        'USPS TRUCK', 'USPS DELIV', 'USPS Truck', 'Usps truck', 'USPS', 'US POSTAL',
        'POSTA', 'Tractor', 'Tract',
        'LARGE COM VEH(6 OR MORE TIRES)', 'TRUCK', 'truck',
        'Dump', 'DUMP', 'DUMP TRUCK', 'dumps',
        'Tanker', 'Tractor Truck Diesel', 'Tractor Truck Gasoline',
        'Tralier', 'Trailer', 'TRAIL', 'trail',
    ],
 
    "Heavy Commercial - Heavy": [
        # true heavy-duty
        'CEMENT TRU', 'Concrete Mixer', 'Const',
        'Garbage or Refuse', 'GARBAGE TR', 'sanit',
        'Lift Boom',
    ],
 
    "Bus": [
        'Bus', 'bus', 'BUS', 'mta bus', 'MTA bus', 'MTA BUS', 'MTA', 'MTA B', 'NY CITY MT',
        'School Bus', 'SCHOOL BUS', 'MINI SCHOO', 'SCHOO', 'mini bus',
    ],
 
    "Emergency / Municipal": [
        'Ambulance', 'AMBULANCE', 'ambulance', 'AMB', 'AMBUL', 'AMBU', 'ambul',
        'X AMB', 'FDNY AMBUL', 'FDNY FIRE', 'FDNY', 'FDNY Truck',
        'Fire Truck', 'FIRE TRUCK', 'FIRE', 'fire',
        'Snow Plow'
    ],
 
    "Motorcycle": [
        'Motorcycle', 'MOTORCYCLE', 'Motorbike',
         'Minicycle', 'Minibike',
    ],
    "Scooter": ['MOPED','Moped', 
        'Scooter', 'scooter', 'SCOOTER', 'SCOOT', 'SCOO', 'scoot', 'Scoot','Motorscooter',
        'E-Scooter', 'E-SCOOTER', 'E-scooter', 'E scooter', 'E SCOOTER', 'e-scooter', 'E-Sco',
        'ELECTRIC S', 'Electric S', 'electric s',
        'REVEL scoo', 'RAZOR SCOO', 'Razor Scoo', 'e sco',    
    ],
 
    "Bike": [
        'Bike', 'Bicycle', 'BICYCLE',
    ],
    "E-Bike": ['E-Bike', 'E-BIKE', 'E-bike', 'e-bike', 'E bike', 'Ebike', 'EBIKE',
        'E-Bik', 'E-BIK', 'E BIK', 'e bik', 'Electric B','e-bik'
    ],
    "Skateboard": [
        'Skateboard', 'SKATEBOARD', 'skateboard', 'E-SKATEBOA', 'skate', 'SKATE'],

    "Other Mobility Vehicles" : ['HOVERBOARD', 'MOTOR UNIC','UNICYCLE',
        'Pedicab', 'PEDICAB', 'pedicab', 'PEDIC', 'pedic',
        'HOSRE DRAW', 'HORSE DRAW', 'Horse carr', 'HORSE', 'Horse', 
    ],

    "Small Speciality Vehicles": [
        'Golf Cart', 'GOLF CART', 'GOLF',
        'Gator 4x4', 'GATOR', 'UTV',
        'FORKLIFT', 'forklift', 'FORKL','Pallet','Carry All'
    ],
 
    "Unknown": [
        'UNK', 'unk', 'UNKNOWN', 'unkno', 'UNKNO', 'NEW Y',
        'Standing S', 'standing s', 'PSD', 'OMT', 'acces',
        'WORKM', 'CUSHM', 'ELECT', 'Marke',
        'FOR', 'For', 'OTHER','cart','MOTOR',
        'Multi-Wheeled Vehicle', 'TOUR',
        'BS','LMB','Motorized','TRANSPORT'
    ],
}
 