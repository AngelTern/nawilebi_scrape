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

def process_year_vgparts(year):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4}|\s*)')
    match = re.search(year_pattern, year)
    if match:
        start_year = match.group(1)
        end_year = match.group(2)
        if end_year:
            return int(start_year), int(end_year)
        else:
            return start_year, None
    else:
        return None, None
    
def process_car_model_topautoparts(car_model):

    match = re.search(r'(\d{2,4})-(\d{2,4}|ON)', car_model)
    
    if match:
        start_year = format_year(match.group(1))
        end_year = match.group(2)
        if end_year == 'ON':
            end_year = datetime.now().year
        else:
            end_year = format_year(end_year)
        
        year_range = f"{start_year}-{end_year}"
        car_model_cleaned = car_model.replace(match.group(0), '').strip()
        return year_range, car_model_cleaned, start_year, end_year
    else:
        return None, car_model, None, None
def process_car_part_full_topautoparts(car_part_full, car_model):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4}|\s*)')
    car_part_full = re.sub(year_pattern, '', car_part_full)
    if car_model:
        car_part_full = car_part_full.replace(car_model, '').strip()
    
    return car_part_full
def adjust_car_model_name_carparts(car_model):
    car_model_lowered = car_model.lower()
    car_model_adjusted = car_model_lowered.replace(" ", "-")
    return car_model_adjusted

def process_car_model_carparts(car_model):
    return re.sub(r'(\b\d{2,4}(?:-\d{2,4})?\b)', '', car_model).strip()

def process_part_full_name_carparts(part_full_name, car_model, car_mark):
    part_full_name_adjusted = re.sub(re.escape(car_model), '', part_full_name, flags=re.IGNORECASE).strip()
    part_full_name_adjusted = re.sub(re.escape(car_mark), '', part_full_name_adjusted, flags=re.IGNORECASE).strip()
    part_full_name_final = re.sub(r'(\b\d{2,4}(?:-\d{2,4})?\b)', '', part_full_name_adjusted).strip()
    return part_full_name_final

def process_year_carparts(year):
    year = year.strip()
    
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4}|\s*)')
    match = year_pattern.search(year)
    
    if match:
        start_year = format_year(match.group(1))  
        end_year = match.group(2).strip() if match.group(2).strip() else None
        if end_year:
            end_year = format_year(end_year)  
    else:
        start_year = format_year(year)
        end_year = None

    return year, start_year, end_year

def process_car_model_vsauto(car_model):
    match = re.search(r'(\d{2,4}-\d{2,4})', car_model)
    if match:
        year_range = match.group(0)
        car_model = car_model.replace(year_range, '').strip()
        return year_range, car_model
    else:
        return None, car_model
    
def process_year_vsauto(year):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4}|\s*)')
    match = re.search(year_pattern, year)
    if match:
        start_year = match.group(1)
        end_year = match.group(2)
        return start_year, end_year
    else: return None, None
    
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

def process_year_partscorner(year):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4})')
    match = year_pattern.search(year)
    
    start_year = None
    end_year = None
    
    if match:
        start_year = format_year(match.group(1))
        end_year = format_year(match.group(2))

    return start_year, end_year


def process_year_goparts(car_model):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4})')
    match = year_pattern.search(car_model)
    
    start_year = None
    end_year = None
    year_range = None
    
    if match:
        start_year = format_year(match.group(1))
        end_year = format_year(match.group(2))
        year_range = f"{start_year}-{end_year}"
        
        # Remove the matched year from car_model string
        car_model = re.sub(match.group(0), '', car_model).strip()
    
    return car_model, start_year, end_year, year_range
    
def process_part_full_name_goparts(part_full_name):
    year_pattern = re.compile(r'(\d{2,4})\s*-\s*(\d{2,4})')
    match = year_pattern.search(part_full_name)
    
    if match:
        return re.sub(match.group(0), '', part_full_name).strip()
    else:
        return part_full_name.strip()

    
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


def parse_price(value):

    if isinstance(value, int) or isinstance(value, float):
        return value  
    
    if not isinstance(value, str):
        return 0.0 
    
    cleaned_string = re.sub(r'[^\d.,]', '', value)
    
    if not cleaned_string:
        return 0.0 
    
    cleaned_string = cleaned_string.replace(',', '.')

    try:
        return float(cleaned_string)
    except ValueError:
        return 0.0 

