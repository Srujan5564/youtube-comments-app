import requests
from urllib.parse import urlparse, parse_qs

# Your API key (replace with your actual API key)
API_KEY = "AIzaSyAagRiklI6MIpYH2_BKRslptAscGGEFA20"

# Function to extract video ID from a YouTube URL
def get_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)
    video_id = None

    # Check if the URL is a standard YouTube link
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            video_id = parse_qs(parsed_url.query).get('v')
            if video_id:
                video_id = video_id[0]
        elif parsed_url.path.startswith('/embed/'):
            video_id = parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            video_id = parsed_url.path.split('/')[2]
    # Check if the URL is a shortened youtu.be link
    elif parsed_url.hostname == 'youtu.be':
        video_id = parsed_url.path[1:]

    if video_id:
        print(f"Extracted video ID: {video_id}")
    else:
        print(f"Failed to extract video ID from URL: {youtube_url}")
    
    return video_id

# Function to get comments
def get_comments(video_url,max_comments, api_key = API_KEY, order='time'):
    comments = []
    video_id = get_video_id(video_url)

    if not video_id:
        print("Invalid YouTube URL")
        return comments

    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key': api_key,
        'textFormat': 'plainText',
        'maxResults': 100,  # Max results per request
        'order': order
    }
    
    # print(f"Request URL: {url}")
    # print(f"Request Params: {params}")

    response = requests.get(url, params=params)
    while response.status_code == 200 and len(comments) < max_comments:
        data = response.json()
        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
            if len(comments) >= max_comments:
                break

        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
            response = requests.get(url, params=params)
        else:
            break

    if response.status_code != 200:
        error_info = response.json()
        print(f"Error: {response.status_code}")
        print(error_info)
        if error_info['error']['errors'][0]['reason'] == 'videoNotFound':
            print("The specified video ID could not be found. Please check the video ID and try again.")
        else:
            print("An error occurred. Please check your API key and other parameters.")
    
    return comments[:max_comments]  # Return up to max_results comments

# # Example YouTube video URL
# VIDEO_URL = 'https://www.youtube.com/watch?v=xIgPMguqyws&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&index=2'

# # Fetch comments using the video URL
# comments = get_comments(VIDEO_URL, API_KEY)
# # for i, comment in enumerate(comments, 1):
# # #     print(f"{i}. {comment}")

# print(comments[0])
# print(len(comments))