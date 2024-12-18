import json
import re

def extract_video_ids(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Use regex to find all videoId values
    video_ids = re.findall(r'"videoId":\s*"([^"]+)"', content)

    return video_ids

def save_video_ids(video_ids, output_file):
    with open(output_file, 'w') as file:
        for video_id in video_ids:
            file.write(video_id + '\n')

if __name__ == "__main__":

    input_files = ['murders_qrels.txt']
    output_files = ['murders_qrels1.txt']

    for input_file, output_file in zip(input_files, output_files):
        
        video_ids = extract_video_ids(input_file)
        save_video_ids(video_ids, output_file)
        
        print(f"Extracted {len(video_ids)} video IDs and saved to {output_file}")