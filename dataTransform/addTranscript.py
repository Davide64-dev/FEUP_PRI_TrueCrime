from youtube_transcript_api import YouTubeTranscriptApi
import json

def download_youtube_captions(video_id, language='en'):
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        transcript_text = map(lambda x: x['text'], transcript)
        transcript = ' '.join(transcript_text).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        return transcript

    except Exception as e:
        print(f"Error: {str(e)}")
        return ""


with open('dataset/true_crime_grouped.json') as f:
    data = json.load(f)

for channel in data:
    print(f"Processing channel: {channel}")
    for video in data[channel]:
        video_id = video['id']
        # skip if transcript is present and not empty
        if 'transcript' in video and video['transcript']:
            continue
        transcript = download_youtube_captions(video_id)
        video['transcript'] = transcript


with open('dataset/true_crime_grouped.json', 'w') as f:
    json.dump(data, f, indent=4)