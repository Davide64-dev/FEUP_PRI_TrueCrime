import json
import os

# Path to your JSON file
json_file_path = '../dataset/true_crime.json'

def remove_unwanted_text(description):
    # Split the description by the line break and look for the first occurrence of '_______'
    split_desc = description.split('_______')
    # Keep only the content before the first '_______'
    return split_desc[0].strip()

def clean_json(json_file_path):
    # Open and load the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate over the items in the JSON
    for key, value in data.items():
        if value.get('Channel') == 'Bailey Sarian':
            description = value.get('Description', '')
            # If the description contains '_______', clean it
            if '_______' in description:
                value['Description'] = remove_unwanted_text(description)
        elif value.get('Channel') == 'JCS - Criminal Psychology':
            # Remove everything after the first '\n' in the description
            if '\n' in value.get('Description', ''):
                value['Description'] = value.get('Description', '').split('\n')[0]

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        clean_json(json_file_path)
        print(f"Descriptions cleaned for channel 'Bailey Sarian' in {json_file_path}.")
    else:
        print(f"File not found: {json_file_path}")
