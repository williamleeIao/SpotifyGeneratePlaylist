import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl
import json
import os

data = {}
data['song_Info'] = []


class YouTube_Operation:

    def __init__(self):
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "client_secret.json"
        self.load_json_file()
        print()

    def load_json_file(self):
        with open(self.client_secrets_file) as json_file:
            self.data = json.load(json_file)
            print(self.data)
            print()

    def create_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        self.youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        return self.youtube_client

    def get_liked_videos(self, youtube_client):
        request = youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            maxResults=50,
            myRating="like"
        )
        response = request.execute()

        print()
        for each_item in response['items']:
            data['song_Info'].append(
                {'song_title': each_item['snippet']['title'],
                 'song_description': each_item['snippet']['description'],
                 # 'song_tag': '  '.join(each_item['snippet']['tags'])
                 }
            )

        # https://www.googleapis.com/youtube/v3/search?pageToken=CBkQAA&part=snippet&maxResults=25&order=relevance&q=site%3Ayoutube.com&topicId=%2Fm%2F02vx4&key={YOUR_API_KEY}
        # Get Current OS
        current_path = os.getcwd()
        # create new file and save as json file
        song_title = current_path + "\\" + 'song_info.json'
        with open(song_title, 'w') as outfile:
            json.dump(data, outfile)
        print()

def main():
    youtube_op = YouTube_Operation()
    client = youtube_op.create_youtube_client()
    youtube_op.get_liked_videos(client)


if __name__ == '__main__':
    main()
