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

def get_digits_after_last_slash(string):
    match = re.match(r"/(\d+)(?=[^/]*$)", string)
    if match:
        return match.group(1)
    return None

def process_part_ful_name_vgparts(car_model):
    match = re.search(r'(\d{4})\s*-\s*(\d{4})', car_model)
    
    if match:
        year = f"{match.group(1)}-{match.group(2)}"
        car_model_cleaned = re.sub(r'\s*\d{4}\s*-\s*\d{4}', '', car_model).strip()
        return year, car_model_cleaned
    else:
        return None, car_model
        
        
def unicode_to_georgian(unicode_str):
    return unicode_str.encode('utf-8').decode('unicode-escape')