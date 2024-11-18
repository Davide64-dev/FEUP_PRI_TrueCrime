import json

# Function to safely convert strings to numeric values
def safe_convert(value, to_type=float, default=0):
    try:
        return to_type(value)
    except (ValueError, TypeError):
        return default

# Load the original JSON structure
with open('../dataset/true_crime_merged.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize a list to hold the flattened data
flattened_data = []

# Process each channel
for channel, videos in data.items():
    for video in videos:
        # Add the channel name to each video entry
        flattened_entry = {
            "Channel": channel,
            **video  # Merge the existing video data
        }

        # Safely convert numeric fields
        flattened_entry["Views"] = safe_convert(flattened_entry.get("Views"), float)
        flattened_entry["Likes"] = safe_convert(flattened_entry.get("Likes"), int)
        flattened_entry["Comments"] = safe_convert(flattened_entry.get("Comments"), int)

        flattened_data.append(flattened_entry)

# Save the flattened data to a new JSON file
with open('../dataset/true_crime_flattened.json', 'w', encoding='utf-8') as file:
    json.dump(flattened_data, file, indent=4, ensure_ascii=False)

# Validate the generated JSON
with open('../dataset/true_crime_flattened.json', 'r') as f:
    try:
        data = json.load(f)
        print("JSON is valid")
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
