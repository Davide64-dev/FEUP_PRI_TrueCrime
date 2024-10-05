from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = "AIzaSyCIYPIUDLfdWq7jkJc8hpfu2OSC4MNkMC8"

youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_id(query):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1
    ).execute()

    for item in search_response['items']:
        video_id = item['id'].get('videoId')
        if video_id:
            return video_id
        
    return ""

def get_video_comments(video_id):
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                pageToken=response['nextPageToken'],
                textFormat="plainText"
            ).execute()
        else:
            break

    df = pd.DataFrame(comments, columns=['comment'])
    df.to_csv(f"{video_id}_comments.csv", index=False)

get_video_comments("SwSbnmqk3zY")