import datetime
current_date = datetime.date.today()

micro_mobility = [
    # E-bikes and bikes (existing)
    'e-scooter','e-bike', 'bike', 'BICYCLE', 'E-Bik', 'E-Sco','E BIK',
    'E-BIK','E-SCOOTER', 'E-scooter', 'e-scooter', 'E scooter', 'E SCOOTER',
    'EBIKE', 'Ebike', 'E-bike', 'E-BIKE', 'E-bike', 'E bike', 'Citi bike',
    'Electric B', 'electric s', 'e-bi', 'e bik', 'e-bike','Bike','BIKE','E-Bike',
    'Bicycle', 'BICYC', 'Bicyc', 'E Sco', 'e sco', 'PEDAL BIKE',
    # Scooter variations (kick/push scooters and e-scooters)
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

injury_types = ['NaN', 'Eye', 'Elbow-Lower-Arm-Hand', 'Knee-Lower Leg Foot', 'Back', 
              'Hip-Upper Leg', 'Shoulder - Upper Arm', 'Unknown', 'Face',
                'Abdomen - Pelvis', 'Neck', 'Chest', 'Does Not Apply', 'Entire Body', 'Head']

complaints = ['NaN', 'Contusion - Bruise', 'Minor Burn', 'Amputation', 'Severe Burn', 
              'None Visible', 'Fracture - Dislocation', 'Fracture - Distorted - Dislocation', 
              'Severe Bleeding', 'Minor Bleeding', 'Internal', 'Whiplash', 'Crush Injuries', 
              'Unknown', 'Complaint of Pain or Nausea', 'Concussion', 'Does Not Apply', 
              'Severe Lacerations', 'Moderate Burn', 'Complaint of Pain', 'Abrasion', 'Paralysis']

emotional_status = ['NaN', 'Unknown', 'Semiconscious', 'Does Not Apply', 'Unconscious', 'Incoherent', 
                    'Apparent Death', 'Conscious', 'Shock']

#vehicles database - h9gi-nx95
#persons database - f55k-p6yu

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
 