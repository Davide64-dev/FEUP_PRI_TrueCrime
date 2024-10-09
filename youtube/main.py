from googleapiclient.discovery import build
import json

with open('config.json') as f:
    config = json.load(f)
api_key = config['YOUTUBE_API_KEY']

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
    comments_data = {}

    response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    index = 1
    while response:
        for item in response['items']:
            # Top-level comment
            top_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_entry = {
                'comment': top_comment,
                'replies': [] 
            }

            if 'replies' in item:
                for reply in item['replies']['comments']:
                    reply_text = reply['snippet']['textDisplay']
                    comment_entry['replies'].append(reply_text)  

            comments_data[str(index)] = comment_entry
            index += 1

        # Check for next page of comments
        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=response['nextPageToken'],
                textFormat="plainText"
            ).execute()
        else:
            break

    with open(f"{video_id}_comments.json", "w", encoding='utf-8') as f:
        json.dump(comments_data, f, ensure_ascii=False, indent=4)



def get_video_thumbnail(video_id):
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    for item in response['items']:
        thumbnail = item['snippet']['thumbnails']['high']['url']
        return thumbnail
    


def get_video_caption_info(video_id):
    response = youtube.captions().list(
        part='snippet',
        videoId=video_id
    ).execute()

    with open(f"{video_id}_captions.json", "w", encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)



#print(get_video_thumbnail(get_video_id("A Killer Deadlier than Hitler? Joseph Stalin Part 2 | Dark History with Bailey Sarian")))
#get_video_comments(get_video_id("A Killer Deadlier than Hitler? Joseph Stalin Part 2 | Dark History with Bailey Sarian"))
#get_video_caption_info(get_video_id("A Killer Deadlier than Hitler? Joseph Stalin Part 2 | Dark History with Bailey Sarian"))
