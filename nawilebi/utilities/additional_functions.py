import re
from datetime import datetime

def extract_numbers(string):
    return re.sub(r'\D', '', string)

def process_car_model_autopia(car_model, car_mark):
    car_model_unchanged = car_model
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{0,4})')
    
    car_model_without_mark = re.sub(re.escape(car_mark), '', car_model, flags=re.IGNORECASE).strip()
    
    car_model_adjusted = re.sub(year_pattern, '', car_model_without_mark).strip()

    return car_model_adjusted, car_model_unchanged



def process_part_full_name_autopia(part_full_name, car_model, car_mark):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{0,4})')
    part_full_name_adjusted = re.sub(re.escape(car_model), '', part_full_name).strip()
    
    part_full_name_adjusted = re.sub(year_pattern, '', part_full_name_adjusted).strip()
    
    part_full_name_adjusted = re.sub(re.escape(car_mark), '', part_full_name_adjusted).strip()    
    
    part_full_name_adjusted = re.sub('-', '', part_full_name_adjusted).strip()
    
    return part_full_name_adjusted


def process_year_autopia(year):
    year_stripped = year.strip()
    current_year = datetime.now().year
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{0,4})')
    match = re.search(year_pattern, year_stripped)

    start_year = None
    end_year = None

    if match:
        start_year = match.group(1)
        end_year = match.group(2) if match.group(2) else current_year
    else:
        try:
            start_year = int(year_stripped)
            end_year = start_year
        except ValueError:
            pass

    return start_year, end_year
    
def get_digits_after_last_slash(string):
    match = re.search(r"/(\d+)(?=[^/]*$)", string)
    if match:
        return match.group(1)
    return None

def get_digits_after_last_equal(string):
    match =re.search(r"=(\d+)(?=[^=]*$)", string)
    if match:
        return match.group(1)
    return None

def process_car_model_vgparts(car_model):
    match = re.search(r'(\d{4})\s*-\s*(\d{4})', car_model)
    
    if match:
        year = f"{match.group(1)}-{match.group(2)}"
        car_model_cleaned = re.sub(r'\s*\d{4}\s*-\s*\d{4}', '', car_model).strip()
        car_model_cleaned = re.sub(r'\s*\(\)\s*$', '', car_model_cleaned)
        return year, car_model_cleaned
    else:
        return None, car_model
        
def process_car_model_topautoparts(car_model):
    match = re.search(r'(\d{2,4}-\d{2,4})', car_model)
    if match:
        year_range = match.group(0)
        car_model = car_model.replace(year_range, '').strip()
        return year_range, car_model
    else:
        return None, car_model

def process_car_part_full_topautoparts(car_part_full, year, car_model):
    car_part_full = car_part_full.replace(year, '').strip()
    car_part_full = car_part_full.replace(car_model, '').strip()
    return car_part_full
        
def adjust_car_model_name_carparts(car_model):
    car_model_lowered = car_model.lower()
    car_model_adjusted = car_model_lowered.replace(" ", "-")
    return car_model_adjusted

def process_car_model_carparts(car_model):
    return re.sub(r'(\b\d{2,4}(?:-\d{2,4})?\b)', '', car_model).strip()

def process_part_full_name(part_full_name, car_model):
    part_full_name_adjusted = re.sub(re.escape(car_model), '', part_full_name, flags=re.IGNORECASE).strip()
    part_full_name_final = re.sub(r'(\b\d{2,4}(?:-\d{2,4})?\b)', '', part_full_name_adjusted).strip()
    return part_full_name_final


def process_car_model_vsauto(car_model):
    match = re.search(r'(\d{2,4}-\d{2,4})', car_model)
    if match:
        year_range = match.group(0)
        car_model = car_model.replace(year_range, '').strip()
        return year_range, car_model
    else:
        return None, car_model
def adjust_for_next_url_autotrans(car_mark, car_model):
    car_mark_adjusted = car_mark.lower()
    car_model_adjusted = re.sub(r"\s+", "-", car_model.lower())
    return car_mark_adjusted, car_model_adjusted

def process_and_clean_car_model_autotrans(car_model):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4})')
    match = year_pattern.search(car_model)
    
    start_year = None
    end_year = None
    
    if match:
        start_year = format_year(match.group(1))
        end_year = format_year(match.group(2))
        year_range = f"{start_year}-{end_year}"
    else:
        year_range = None

    cleaned_car_model = re.sub(year_pattern, '', car_model).strip()

    return start_year, end_year, cleaned_car_model


def process_part_full_name_carline(part_full_name, car_model, car_mark):
    part_full_name_1 = re.sub(car_model, '', part_full_name, flags=re.IGNORECASE).strip()
    part_full_name_2 = re.sub(car_mark, '', part_full_name_1, flags=re.IGNORECASE).strip()
    year_pattern = re.compile(r'(\d{2,4})')
    part_full_name_adjusted = re.sub(year_pattern, '', part_full_name_2).replace('-', '').strip()
    return part_full_name_adjusted
    
def clean_car_model_carline(car_model, car_mark):
    if car_mark == "CHEVROLET":
        car_model_adjusted = re.sub("CHEVY", '', car_model).strip()
    else:
        car_model_adjusted = re.sub(car_mark, '', car_model).strip()
    year_pattern = re.compile(r'\d{2,4}')
    match = year_pattern.search(car_model)
    if match:
        year_string = match.group()
        return year_string, re.sub(year_string, '', car_model_adjusted).strip()
    return None, car_model

def process_kia_carline(part_full_name):
    pattern_1 = re.compile(r"(SOUL 2009)")
    pattern_2 = re.compile(r"(CERATO)")
    
    match_1 = pattern_1.search(part_full_name)
    match_2 = pattern_2.search(part_full_name)
    
    if match_1:
        car_model = match_1.group()
        return car_model, re.sub(car_model, '', part_full_name).replace('-', '').strip()
    
    elif match_2:
        car_model = match_2.group()
        return car_model, re.sub(car_model, '', part_full_name).replace('-', '').strip()
    
    return None, part_full_name

        

'''---------------------------------------------------------'''

def format_year(year):
    year = int(year)
    if year < 100:
        if year >= 50:
            return 1900 + year
        else:
            return 2000 + year
    return year

def unicode_to_georgian(unicode_str):
    return unicode_str.encode('utf-8').decode('unicode-escape')

import re

def parse_price(value):
    """
    Parse price value, removing non-numeric characters and handling empty or invalid values.
    """
    if isinstance(value, int) or isinstance(value, float):
        return value  # If it's already a number, return it as is
    
    if not isinstance(value, str):
        return 0.0  # Return 0.0 for non-string values
    
    # Clean the price string by removing all non-numeric characters except commas and dots
    cleaned_string = re.sub(r'[^\d.,]', '', value)
    
    # Handle cases where cleaned string is empty or invalid
    if not cleaned_string:
        return 0.0  # Return 0.0 if the cleaned string is empty
    
    # Convert cleaned string to float (handle commas as decimal points)
    try:
        return float(cleaned_string.replace(',', '.'))
    except ValueError:
        return 0.0  # Return 0.0 if conversion to float fails

