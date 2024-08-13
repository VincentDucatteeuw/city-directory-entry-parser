import json
import re
import difflib

input_file = r"C:\Users\vducatte\OneDrive - UGent\Documents\GitHub\city-directory-entry-parser\data\ghent-city-directories\wegwijzer-1913-output-valid-json.txt"
output_file = r"C:\Users\vducatte\OneDrive - UGent\Documents\GitHub\city-directory-entry-parser\data\ghent-city-directories\wegwijzer-1913-output-cleaned.json"

def clean_json_file(input_file, output_file):
    cleaned_data = []
    with open(input_file, 'r', encoding='utf-16') as infile:
        for line in infile:
            # Split the line by commas and process each JSON object separately
            json_objects = line.strip().split('},')
            for json_object in json_objects:
                if not json_object.endswith('}'):
                    json_object += '}'
                try:
                    data = json.loads(json_object)
                    
                    # Clean subjects
                    data['subjects'] = [clean_subject(subject) for subject in data['subjects']]
                    
                    # Clean statuses
                    data['statuses'] = [clean_status(status) for status in data['statuses']]
                    
                    # Clean occupations
                    data['occupations'] = [clean_occupation(occupation) for occupation in data['occupations']]
                    
                    # Clean locations
                    data['locations'] = [clean_location(location) for location in data['locations']]
                    
                    # Clean municipalities
                    data['municipalities'] = [clean_municipality(municipality) for municipality in data['municipalities']]
                    
                    # Add cleaned data to list
                    cleaned_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {json_object}")
                    print(f"Error message: {e}")
    
    # Write the cleaned data back to the output file as a JSON array
    with open(output_file, 'w', encoding='utf-16') as outfile:
        json.dump(cleaned_data, outfile, indent=4)


def clean_subject(data):
    data = data.strip()
    return data

def clean_status(data):
    data = data.strip().lower()

    # Define status standardization
    status_mappings = {
        'weduwe': r'^w(ed|eduwe)\.?$',
        'juffrouw': r'^juff(r\.?)?$',
        'huisvrouw': r'^h(uisvr?|vr)\.?$',
        'mevrouw': r'^me?vr\.?$', 
    }

    # Check for matches using regex patterns
    for standardised_status, pattern in status_mappings.items():
        if re.match(pattern, data):
            return standardised_status
    return data  # Return original data if no match found

def clean_occupation(data):
    data = data.strip()
    return data

def clean_location(location):
    # Ensure location is a dictionary with a 'value' key
    if not isinstance(location, dict) or 'value' not in location or not isinstance(location['value'], str):
        raise ValueError("Invalid location format. Expected a dictionary with a 'value' key containing a string.")
    
    location['value'] = location['value'].strip()
    location['value'] = re.sub(r'(\w+str)\.?', r'\1aat', location['value']) # Replace 'str.' with 'straat'
    location['value'] = re.sub(r'(\w+steenw)\.?', r'\1eg', location['value']) # Replace 'steenw.' with 'steenweg'
    location['value'] = re.sub(r"stw\.?", "steenweg", location['value']) # Replace 'stw.' with 'steenweg'
    location['value'] = re.sub(r'(\w+pl)\.?', r'\1aats', location['value']) # Replace 'pl.' with 'plaats'
    location['value'] = re.sub(r's\.?\s', "Sint", location['value']) # Replace 's.' with 'Sint'
    location['value'] = re.sub(r'denderm\.?\s', "Dendermondsche", location['value']) # Replace 'denderm.' with 'Dendermondsche'
    location['value'] = re.sub(r'hundelg\.?\s', "Hundelgemsche", location['value']) # Replace 'hundelg.' with 'Hundelgemsche'
    location['value'] = re.sub(r'otterg\.?\s', "Ottergemsche", location['value']) # Replace 'otterg.' with 'Ottergemsche'
    location['value'] = re.sub(r'antw\.?\s', "Antwerpsche", location['value']) # Replace 'antw.' with 'Antwerpsche'
    return location

def clean_municipality(data):
    data = data.strip()
    return data

# Call the function to clean the JSON file
clean_json_file(input_file, output_file)
def clean_status(data):
    data = data.strip().lower()

    # Define status standardization
    status_mappings = {
        'weduwe': r'^w(ed|eduwe)\.?$',
        'juffrouw': r'^juff(r\.?)?$',
        'huisvrouw': r'^h(uisvr?|vr)\.?$',
        'mevrouw': r'^me?vr\.?$', 
    }

    # Check for matches using regex patterns
    for standardised_status, pattern in status_mappings.items():
        if re.match(pattern, data):
            return standardised_status
    return data  # Return original data if no match found

def clean_occupation(data): # TO DO
    data = data.strip().lower()
    data = re.sub(r'-', ' ', data)  # Replace hyphens with spaces
    # Add more specific cleaning rules for occupations
    return data

def clean_location(data): # DONE
    data['value'] = data['value'].strip()

    data = re.sub(r'(\w+str)\.?\s', r'\1aat', data) # Replace 'str.' with 'straat'

    data = re.sub(r'(\w+steenw)\.?\s', r'\1eg', data) # Replace 'steenw.' with 'steenweg'
    data = re.sub(r"stw\.?", "steenweg", data) # Replace 'stw.' with 'steenweg'

    data = re.sub(r'(\w+pl)\.?\s', r'\1aats', data) # Replace 'pl.' with 'plaats' # Issue that 'pl' is also in 'plein'

    data = re.sub(r's\.?\s', "Sint", data) # Replace 's.' with 'Sint

    data = re.sub(r'denderm\.?\s', "Dendermondsche", data) # Replace 'denderm.' with 'Dendermondsche'
    data = re.sub(r'hundelg\.?\s', "Hundelgemsche", data) # Replace 'hundelg.' with 'Hundelgemsche'
    data = re.sub(r'otterg\.?\s', "Ottergemsche", data) # Replace 'otterg.' with 'Ottergemsche'
    data = re.sub(r'antw\.?\s', "Antwerpsche", data) # Replace 'antw.' with 'Antwerpsche'
    return location


def clean_municipality(data): # DONE
    data = data.strip().lower()

    # Define standard municipality names
    standard_municipalities = [
        'afsnee',
        'desteldonk',
        'drongen',
        'gentbrugge',
        'ledeberg',
        'mariakerke',
        'mendonk',
        'oostakker',
        'sint-amandsberg',
        'sint-denijs-westrem',
        'sint-kruis-winkel',
        'wondelgem',
        'zwijnaarde'
    ]

    # Remove periods and handle common abbreviations
    data = re.sub(r'\.', '', data)  # Remove all periods
    data = re.sub(r'^s\s?am', 'sint-amand', data)  # Replace 's am' with 'sint-amand'
    data = re.sub(r'^st\s?', 'sint-', data)  # Replace 'st ' with 'sint-'

    # Use difflib to find closest match
    matches = difflib.get_close_matches(data, standard_municipalities, n=1, cutoff=0.6)
    
    if matches:
        data = matches[0].title()  # Convert the first match to title case
    else:
        data = data  # Return the original data if no match is found
    
    return data

# Usage
input_file = "C:/Users/vducatte/OneDrive - UGent/Documents/GitHub/city-directory-entry-parser/data/ghent-city-directories/wegwijzer-1913-output.json"
output_file = "C:/Users/vducatte/OneDrive - UGent/Documents/GitHub/city-directory-entry-parser/data/ghent-city-directories/wegwijzer-1913-cleaned-output.json"
clean_json_file(input_file, output_file)