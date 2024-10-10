import json
import os

# Path to your JSON file
json_file_path = '../dataset/true_crime.json'

def group_by_channel(json_file_path):
    # Open and load the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create a dictionary to store videos grouped by channel
    channel_data = {}

    # Iterate over the items in the JSON
    for key, value in data.items():
        channel = value.get('Channel')
        if channel not in channel_data:
            channel_data[channel] = []
        # Remove the 'Channel' and 'Month' keys from the value
        value.pop('Channel', None)
        value.pop('Month', None)
        channel_data[channel].append(value)

    # Write the grouped data to a new JSON file
    with open('../dataset/true_crime_grouped.json', 'w', encoding='utf-8') as file:
        json.dump(channel_data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        group_by_channel(json_file_path)
        print(f"Videos grouped by channel in {json_file_path}.")
    else:
        print(f"File not found: {json_file_path}")