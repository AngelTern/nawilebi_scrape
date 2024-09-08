import re

def extract_numbers(string):
    return re.sub(r'\D', '', string)

def process_part_full_name_autopia(part_full_name, year, car_mark):
    
    if "სატესტო" in part_full_name:
        return None, None
    
    year_pattern = re.compile(re.escape(year))  
    modified_string = year_pattern.sub('', part_full_name).strip()  
    
    modified_string = modified_string.rstrip('-').strip()

    if "-" in modified_string:
        split_values = modified_string.split("-", 1)  
        part_name = split_values[0].strip()  
        car_model = split_values[1].strip()
        car_model = car_model.replace(car_mark, '').strip()
        
    else:
        part_name = modified_string 
        car_model = "" 

    return part_name, car_model