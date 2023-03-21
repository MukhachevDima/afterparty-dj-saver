from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the credentials flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', scopes=['https://www.googleapis.com/auth/youtube']
)
creds = Credentials.from_authorized_user_info(info={}, scopes=['https://www.googleapis.com/auth/youtube'])

# Set up the YouTube API client
youtube = build('youtube', 'v3', credentials=creds)

# Search for a video by name
query = 'Your video name here'
search_response = youtube.search().list(
    q=query,
    type='video',
    part='id,snippet',
    maxResults=10
).execute()

# Get the first video from the search results
video_id = search_response['items'][0]['id']['videoId']
video_title = search_response['items'][0]['snippet']['title']

# Add the video to a playlist
playlist_id = 'Your playlist ID here'
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
