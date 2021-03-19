import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from settings import VIDEO_ID


def auth_on_youtube():
    credentials = None

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # Google's Request
    from google.auth.transport.requests import Request

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=[
                    'https://www.googleapis.com/auth/youtube'
                ]
            )

            flow.run_local_server(port=8080, prompt='consent',
                                  authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    return credentials


def get_client(credentials):
    return build("youtube", "v3", credentials=credentials)


def get_video_views(client, video_id):
    response = client.videos().list(part="statistics", id=video_id).execute()
    return int(response["items"][0]["statistics"]["viewCount"])


def update_video_title(client, video_id, title):
    response = client.videos().update(
        part="snippet",
        body={"id": video_id,
              "snippet": {
                  "title": title,
                  "categoryId": 28, }
              }
    ).execute()
    print(response)


def main():
    credentials = auth_on_youtube()
    if credentials:
        client = get_client(credentials)
        video_views = get_video_views(client, VIDEO_ID)
        update_video_title(client, VIDEO_ID, "Este Vídeo Tem {} Visualizações".format(video_views))


if __name__ == "__main__":
    main()
