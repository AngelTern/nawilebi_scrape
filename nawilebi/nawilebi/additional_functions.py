import re

def extract_numbers(string):
    return re.sub(r'\D', '', string)

def process_part_full_name(part_full_name, year):
    # Step 1: Remove the year and any adjacent hyphen or space from part_full_name
    year_pattern = re.compile(re.escape(year))  # Escape the year to match it literally
    modified_string = year_pattern.sub('', part_full_name).strip()  # Remove the year
    
    # Remove trailing hyphen if any after removing the year
    modified_string = modified_string.rstrip('-').strip()

    # Step 2: Separate Georgian and English words
    georgian_words = []
    english_words = []

    words = modified_string.split()

    for word in words:
        if re.match(r'^[\u10A0-\u10FF]+$', word):  # Georgian word (Unicode for Georgian characters)
            georgian_words.append(word)
        else:  # English word (car model)
            english_words.append(word)

    # Step 3: Combine Georgian words back into a single string and English words into car_model
    georgian_string = ' '.join(georgian_words).strip()
    car_model = ' '.join(english_words).strip()

    return georgian_string, car_model