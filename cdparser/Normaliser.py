import json
import re
import difflib

def clean_json_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
            data = json.load(infile)

            # Ensure data is a list of dictionaries
            for entry in data:
        
                # Clean subjects
                entry['subjects'] = [clean_subject(subject) for subject in entry['subjects']]
                        
                # Clean statuses
                entry['statuses'] = [clean_status(status) for status in entry['statuses']]
                        
                # Clean occupations
                entry['occupations'] = [clean_occupation(occupation) for occupation in entry['occupations']]
                        
                # Clean locations
                entry['locations'] = [clean_location(location) for location in entry['locations']]
                        
                # Clean municipalities
                entry['municipalities'] = [clean_municipality(municipality) for municipality in entry['municipalities']]
                        
                # Write the cleaned data back to the output file
                json.dump(data, outfile)
                outfile.write('\n')

        # Write the cleaned data back to the output file
        with open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)  # Added `ensure_ascii=False` for non-ASCII characters

    except json.JSONDecodeError as e:
        print(f"Skipping invalid JSON: {e}")

def clean_subject(entry):

    # Apply all the replacements
    replacements = [
        (r'\s\.', '.'), # Remove spaces before periods
        (r'\s\,', ','), # Remove spaces before commas
        (r'\s\),', ')'), # Remove spaces before closing parentheses
        (r'\,$', '.'), # Replace trailing ',' with '.'
        (r'([A-Z])$', r'\1.'), # Add a period at the end of the string if it's a single capital letter
        (r'(?<!\ben\s)zust\.?$', 'zusters'), # Replace 'zust.' with 'zusters'
        (r'en\s?zust\.?$', 'en zuster'), # Replace 'en zust.' with 'en zusters'
        (r'gebroed$', 'gebroeders'), # Replace 'gebroed' with 'gebroeders'
        (r'broed\.?$', 'broeders'), # Replace 'broed.' with 'broeders'
        (r'naaml\.? maatsch\.?', 'naamloze maatschappij'), # Replace 'naaml. maatsch.' with 'naamlooze maatschappij'
        ]

    for pattern, replacement in replacements:
        entry = re.sub(pattern, replacement, entry)

    return entry

def clean_status(entry):
    entry = entry.strip().lower()
    entry = re.sub(r'\s\.', '.', entry)  # Remove spaces before periods

    # Define status standardization
    standardised_statuses = {
        'weduwe': r'^w(ed|eduwe)\.?$',
        'juffrouw': r'^juffr?\.?$',
        'huisvrouw': r'^h(uisvr?|vr)\.?$',
        'mevrouw': r'^me?vr\.?$', 
    }

    # Check for matches using regex patterns
    for standardised_status, pattern in standardised_statuses.items():
        if re.match(pattern, entry):
            return standardised_status
    return entry  # Return original data if no match found

def clean_occupation(entry):
    # Apply all the replacements

    replacements = [
        (r'\s\.', '.'), # Remove spaces before periods
        (r'\s\,', ','), # Remove spaces before commas
        (r'\s\),', ')'), # Remove spaces before closing parentheses
        (r'\,$', '.'), # Replace trailing ',' with '.'
        (r'^\s', ''), # Remove leading whitespace
        (r'herberg(\.|$)', 'herbergier'),
        (r'herb\.?$', 'herbergier'),
        (r'mekaniekmak.', 'mekaniekmaker'),
        (r'elledgoed\.?$', 'elledgoedmaker'),
        (r'bijzonder\.?$', 'bijzondere'),
        (r'vleeschh\.?$', 'vleeschhouwer'),
        (r'varkenssl\.?$', 'varkensslachter'),
        (r'kleerm(\.|ak\.)$', 'kleermaker'),
        (r'katoenspin.', 'katoenspinnerij'),
        (r'houth\.?$', 'houthandelaar'),
        (r'kolenk\.?$', 'kolenkoopman'),
        (r'koopm.', 'koopman'),
        (r'handelsvertegenw.', 'handelsvertegenwoordiger'),
        (r'modew.', 'modewaren'),
        (r'vischhandel.', 'vischhandelaar'),
        (r'policiecommiss.', 'politiecommissaris'),
        (r'beschuitfabrik.', 'beschuitfabrikant'),
        (r'wijsbeg.', 'wijsbegeerte'),
        (r'meubelm.', 'meubelmaker'),
        (r'foorereiz.', 'foorereiziger'),
        (r'provinc best.', 'provinciaal bestuur'),
        ]

    for pattern, replacement in replacements:
        entry = re.sub(pattern, replacement, entry)

    return entry

def clean_location(entry):
    if isinstance(entry, dict):
        # If entry is a dictionary, process each value
        return {k: clean_location(v) for k, v in entry.items()}
    elif isinstance(entry, str):
        # If entry is a string, process it as before
        entry = entry.strip()
        
        # Apply all the replacements
        replacements = [
            (r'\s\.', '.'), # Remove spaces before periods
            (r'(str)\.?(\s|$)', r'\1aat '), # Replace 'str' with 'straat '
            (r'(steenw)\.?(\s|$)', r'\1eg '), # Replace 'steenw' with 'steenweg '
            (r'stn?w\.?(\s|$)', 'steenweg '), # Replace 'st(n)w' with 'steenweg '
            (r'(\w+pl)\.?(\s|$)', r'\1aats '), # Replace 'pl' with 'plaats ' # check how to deal with 'plein'
            (r'denderm\.?\s', 'dendermondsche '), # Replace 'denderm' with 'dendermondsche '
            (r'hundelg\.?\s', 'hundelgemsche '), # Replace 'hundelg' with 'hundelgemsche '
            (r'otterg\.?\s', 'ottergemsche '), # Replace 'otterg' with 'ottergemsche '
            (r'antw\.?\s', 'antwerpsche '), # Replace 'antw' with 'antwerpsche '
            (r'bruss\.?\s', 'brusselsche '), # Replace 'bruss' with 'brusselsche '
            (r'kortr\.?\s', 'kortrijksche '), # Replace 'kortr' with 'kortrijksche '
            (r'drong\.?\s', 'drongensche '), # Replace 'drong' with 'drongensche '
            (r'meulest\.?\s', 'meulesteedsche '), # Replace 'meulest' with 'meulesteedsche '
            (r'\bs\.\s', 'sint ') # Replace 's.' with 'sint '
        ]
        
        for pattern, replacement in replacements:
            entry = re.sub(pattern, replacement, entry)
        
        return entry
    else:
        # If data is neither a dict nor a string, return it as is
        return entry


def clean_municipality(entry): # DONE
    entry = entry.strip().lower()

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
    entry = re.sub(r'\.', '', entry)  # Remove all periods
    entry = re.sub(r'^s\s?am', 'sint-amand', entry)  # Replace 's am' with 'sint-amand'
    entry = re.sub(r'^st\s?', 'sint-', entry)  # Replace 'st ' with 'sint-'

    # Use difflib to find closest match
    matches = difflib.get_close_matches(entry, standard_municipalities, n=1, cutoff=0.6)
    
    if matches:
        entry = matches[0].title()  # Convert the first match to title case
    else:
        entry = entry  # Return the original data if no match is found
    
    return entry

# Usage
input_file = r'C:\Users\vducatte\OneDrive - UGent\Documents\GitHub\city-directory-entry-parser\CRF_output.json'
output_file = 'cleaned_output.json'
clean_json_file(input_file, output_file)