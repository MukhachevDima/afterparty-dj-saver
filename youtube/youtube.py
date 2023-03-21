from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


with open('client_api.txt', 'r') as file:
    api_key = file.read().rstrip()
# Set up the YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

with open('../play.list', 'r') as file:
    temp = file.read()
    play_list = temp.split('\n')

# Search for a video by nameimpr
for song in play_list:
    if song[0] ==  '#':
        continue
    search_response = youtube.search().list(
        q=song,
        type='video',
        part='id,snippet',
        maxResults=10
    ).execute()

    # Get the first video from the search results
    video_id = search_response['items'][0]['id']['videoId']
    video_title = search_response['items'][0]['snippet']['title']

    # Add the video to a playlist
    playlist_id = 'PLJ_lAwHSNYgnJojhzq7Nx_tDapWzn9Dl9'
    playlist_response = youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                },
                'title': video_title
            }
        }
    ).execute()

    print(f'The video "{video_title}" has been added to the playlist "{playlist_response["snippet"]["title"]}"')
