## this will find the videoId from the dataset in dataset/true_crime_flattened.json
## of the video titles that are in videotitles.txt and write them to a file called qrels.txt

# the videotitles.txt file is a text file with the following format:
# "videoTitle1"
# "videoTitle2"
# "videoTitle3"
# ...

import json
import sys

# Load the video titles from the videotitles file
with open("videotitles.txt") as f:
    videostitles = f.readlines()

# strip the newline characters from the video titles and quotes
videostitles = [title.strip().strip('"') for title in videostitles]

# Load the videos from the dataset
with open("dataset/true_crime_flattened.json") as f:
    videos = json.load(f)


# find the videos whose title is in the videotitles file
video_ids = []
for video in videos:
    print(video["Title"])
    if video["Title"] in videostitles:
        video_ids.append(video["videoId"])

# Write the video IDs to the qrels file
with open("qrels.txt", "w") as f:
    for video_id in video_ids:
        f.write(f"{video_id}\n")

print(f"Found {len(video_ids)} video IDs in the dataset.")