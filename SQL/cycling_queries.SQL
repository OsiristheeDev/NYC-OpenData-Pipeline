/* I want to create a new column based on serious injuries */
SELECT *
FROM (SELECT emotional_status,complaint,bodily_injury,collision_id,
CASE WHEN emotional_status IN ('Apparent Death','Unconscious','Semiconscious','Incoherent') OR
    complaint IN('Amputation','Concussion','Internal','Severe Bleeding',
                   'Severe/Moderate/Burn','Fracture-Dislocation') OR 
    bodily_injury = 'Eye' THEN 'Yes'
    ELSE 'No'
    END AS severe_injury,
CASE WHEN safety_equipment IN ('Helmet Only (In-Line Skater/Bicyclist)',
                              'Helmet/Other (In-Line Skater/Bicyclist)')
                              AND person_type IN ('Bicyclist','Other Motorized')
    THEN 'Yes'
    WHEN safety_equipment IN ('None') AND person_type IN ('Bicyclist','Other Motorized')
    THEN 'No'
    END AS wearing_helmet
FROM nyc.collisions_persons)
WHERE severe_injury = 'Yes';

