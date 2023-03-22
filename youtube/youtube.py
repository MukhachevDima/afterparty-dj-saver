from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from time import sleep


# Set up the credentials flow
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', scopes=['https://www.googleapis.com/auth/youtube']
)
creds = flow.run_console()
# Set up the YouTube API client
youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)
# Search for a video by name
i = 0
for line in open('../play.list', 'r'):
    song = line.strip()
    if song.startswith('#') or song.strip() == '':
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
    print(video_title)
    # Add the video to a playlist
    playlist_id = 'PLJ_lAwHSNYgkU6jJTZzdTlC90TDyXj0-C'
    playlist_response = youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': playlist_id,
                'position': i,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                },
                'title': video_title
            }
        }
    ).execute()
    i += 1
    sleep(1)
    print(f'The video "{video_title}" has been added to the playlist "{playlist_response["snippet"]["title"]}"')