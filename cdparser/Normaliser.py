import json
import re
import difflib

def clean_json_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            try:
                data = json.loads(line)
                
                # Clean subjects
                data['subjects'] = [clean_subject(subject) for subject in data['subjects']]
                
                # Clean statuses
                data['statuses'] = [clean_status(status) for status in data['statuses']]
                
                # Clean occupations
                data['occupations'] = [clean_occupation(occupation) for occupation in data['occupations']]
                
                # Clean locations
                data['locations'] = [clean_location(location) for location in data['locations']]
                
                # Clean municipalities
                data['municipalties'] = [clean_municipality(municipality) for municipality in data['municipalties']]
                
                # Write the cleaned data back to the output file
                json.dump(data, outfile)
                outfile.write('\n')
            
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line}")

def clean_subject(data): # TO DO
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

def clean_occupation(data): # TO DO
    data = data.strip().lower()
    data = re.sub(r'-', ' ', data)  # Replace hyphens with spaces
    # Add more specific cleaning rules for occupations
    return data

def clean_location(data): # DONE
    data = data.strip()

    data = re.sub(r'(\w+str)\.?', r'\1aat', data) # Replace 'str.' with 'straat'

    data = re.sub(r'(\w+steenw)\.?', r'\1eg', data) # Replace 'steenw.' with 'steenweg'
    data = re.sub(r"stw\.?", "steenweg", data) # Replace 'stw.' with 'steenweg'

    data = re.sub(r'(\w+pl)\.?', r'\1aats', data) # Replace 'pl.' with 'plaats' # Issue that 'pl' is also in 'plein'

    data = re.sub(r's\.?\s', "Sint", data) # Replace 's.' with 'Sint

    data = re.sub(r'denderm\.?\s', "Dendermondsche", data) # Replace 'denderm.' with 'Dendermondsche'
    data = re.sub(r'hundelg\.?\s', "Hundelgemsche", data) # Replace 'hundelg.' with 'Hundelgemsche'
    data = re.sub(r'otterg\.?\s', "Ottergemsche", data) # Replace 'otterg.' with 'Ottergemsche'
    data = re.sub(r'antw\.?\s', "Antwerpsche", data) # Replace 'antw.' with 'Antwerpsche'


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
input_file = "/home/bavercru/Documents/Visual Code - workspace/CRF/CRF_output.json"
output_file = 'cleaned_output.json'
clean_json_file(input_file, output_file)