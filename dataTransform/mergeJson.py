import json

# Load the JSON files
with open('../dataset/true_crime_grouped.json', 'r') as f:
    grouped_data = json.load(f)

with open('../dataset/true_crime_comments.json', 'r') as f:
    comments_data = json.load(f)

# Initialize the merged dictionary
merged_data = {}

# Iterate over the grouped data
for channel, videos in grouped_data.items():
    merged_data[channel] = []
    # Process each video
    for video in videos:
        video_id = video.get("id")
        # Search for the matching video in comments_data
        matching_video = next(
            (v for v in comments_data.get(channel, []) if v.get("id") == video_id),
            None
        )
        # Merge data
        merged_video = video.copy()
        merged_video["transcript"] = video.get("transcript", "")
        merged_video["comments"] = (
            matching_video.get("comments", []) if matching_video else []
        )
        merged_data[channel].append(merged_video)

# Save the merged data to a new JSON file
with open('../dataset/true_crime_merged.json', 'w') as f:
    json.dump(merged_data, f, indent=4)
