import json
import unicodedata

def load_json_data(filename):
    """Load data from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def normalize_string(text):
    """Normalize strings by removing Turkish characters and accents."""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def determine_school_type(school_name):
    """Determine the type of school based on its name."""
    if not school_name:
        return "Other"
    school_name = normalize_string(school_name.lower())
    if "lise" in school_name:
        return "High School"
    if "ortaokul" in school_name:
        return "Middle School"
    if "ilkokul" in school_name:
        return "Primary School"
    if "anaokulu" in school_name:
        return "Preschool"
    return "Other"

# Input and output file paths
input_filename = 'okullar.json'
output_filename = 'processed_schools.json'

data = load_json_data(input_filename)

school_types_count = {
    "High School": 0,
    "Middle School": 0,
    "Primary School": 0,
    "Preschool": 0,
    "Other": 0
}

processed_data = []
for school in data:
    city = school.get("il", "").strip() if school.get("il") else ""
    school_entry = {
        "city": city,
        "district": school.get("ilce", ""),
        "school_name": school.get("okulAdi", ""),
        "school_info_link": school.get("okulBilgisiLink", ""),
        "school_location_link": school.get("okulKonumuLink", ""),
        "type": determine_school_type(school.get("okulAdi", ""))
    }
    school_types_count[school_entry["type"]] += 1
    processed_data.append(school_entry)

total_schools = len(processed_data)

print(f"Total number of schools: {total_schools}")
for school_type, count in school_types_count.items():
    print(f"{school_type}: {count}")

with open(output_filename, 'w', encoding='utf-8') as output_file:
    json.dump(processed_data, output_file, ensure_ascii=False, indent=4)

print(f"\nProcessed data has been written to {output_filename}")
