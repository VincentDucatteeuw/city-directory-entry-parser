import json
import re
import difflib

def clean_subject(value): # # DONE
    value = value.strip()
    value = re.sub(r'\s+', ' ', value)  # Replace multiple spaces with a single space
    value = re.sub(r'\(firma\)$', '', value)  # Remove "(firma)" at the end
    value = re.sub(r'[.,;:!?]+$', '', value)  # Remove trailing punctuation
    return value

def clean_status(value):
    value = value.strip().lower()

    # Define status standardization
    status_mappings = {
        'weduwe': r'^w(ed|eduwe)\.?$',
        'juffrouw': r'^juff(r\.?)?$',
        'huisvrouw': r'^h(uisvr?|vr)\.?$',
        'mevrouw': r'^me?vr\.?$', 
    }

    # Check for matches using regex patterns
    for standardised_status, pattern in status_mappings.items():
        if re.match(pattern, value):
            return standardised_status
    return value  # Return original value if no match found

value = clean_status(value) # Recursively clean the value

def clean_occupation(value): # TO DO
    value = value.strip().lower()
    value = re.sub(r'-', ' ', value)  # Replace hyphens with spaces
    # Add more specific cleaning rules for occupations
    return value

def clean_location(value): # TO DO
    value = value.strip().lower()
    value = re.sub(r'\s+', ' ', value)  # Replace multiple spaces with a single space
    # Add more specific cleaning rules for locations
    return value

def clean_municipality(value): # DONE
    value = value.strip().lower()

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
    value = re.sub(r'\.', '', value)  # Remove all periods
    value = re.sub(r'^s\s?am', 'sint-amand', value)  # Replace 's am' with 'sint-amand'
    value = re.sub(r'^st\s?', 'sint-', value)  # Replace 'st ' with 'sint-'

    # Use difflib to find closest match
    matches = difflib.get_close_matches(value, standard_municipalities, n=1, cutoff=0.6)
    
    if matches:
        value = matches[0].title()  # Convert the first match to title case
    else:
        value = value  # Return the original value if no match is found
    
    return value
    value = clean_municipality(value)  # Recursively clean the value

print(value)







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
                data['locations'] = [{"value": clean_location(location['value'])} for location in data['locations']]
                
                # Clean municipalities
                data['municipalties'] = [clean_municipality(municipality) for municipality in data['municipalties']]
                
                # Write the cleaned data back to the output file
                json.dump(data, outfile)
                outfile.write('\n')
            
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line}")

# Usage
input_file = 'input.json'
output_file = 'cleaned_output.json'
clean_json_file(input_file, output_file)