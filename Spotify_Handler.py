import spotipy
import requests
import spotipy.util as util
from secrets import user_name, clientId, clientSecret, redirect_uri, spotify_user_id
import json
from time import sleep

CACHE = r"C:\Users\willlee\AppData\Local\Programs\Python\Python37-32\.cache-William Lee"


class Spotify_Operation:

    def __init__(self, scope='playlist-modify'):
        # self.token = self.create_token(scope=scope)
        self.auth_info = self.create_token(scope=scope)
        self.tokenInfo = self.auth_info.get_cached_token()
        self.token = self.tokenInfo['access_token']

    def create_token(self, scope):
        sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=clientId, client_secret=clientSecret,
                                               redirect_uri=redirect_uri, scope=scope, cache_path=CACHE)
        return sp_oauth

    def create_token_depreciated(self, scope):
        token = util.prompt_for_user_token(username=user_name,
                                           scope=scope,
                                           client_id=clientId,
                                           client_secret=clientSecret,
                                           redirect_uri=redirect_uri)
        return token

    def token_is_expired(self):
        return self.auth_info.is_token_expired(self.tokenInfo)

    def read_token(self):
        print(self.token)

    def refresh_token(self):
        # if self.auth_info.is_token_expired(self.tokenInfo):
        token_information = self.auth_info.refresh_access_token(self.tokenInfo['refresh_token'])
        self.tokenInfo = token_information
        self.token = token_information['access_token']
        print()
        # sp = spotipy.Spotify(auth=self.token)  should not be needed

    def create_playlist(self, playlist_name="Youtube Liked Vids", description="All Liked Youtube Videos"):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": playlist_name,
            "description": description,
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            clientId)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)  # self.token is OAuth Token
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    def get_song_from_platlist(self, playlist_id):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id,
        )

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )

        response_json = response.json()
        list_track = [individual['track']['name']for individual in response_json['items']]

        print(list_track)
        return list_track

    def add_song_to_playlist(self, song_id, playlist_id):
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            playlist_id,
            song_id
        )
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()
        # something to handler

    def get_playlists_items(self, playlist_id, search=''):
        """Song name in the playlist"""
        track = []
        query = "https://api.spotify.com/v1/playlists/{}/tracks?market=TW".format(
            playlist_id
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()
        for item in response_json['items']:
            track.append(item['track'])
        return track

    def get_playlist_id(self, user_id, search_name='Youtube Liked Vids'):
        playlist_uri = ''
        """Search for Playlist id"""
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            user_id
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )

        response_json = response.json()
        for playlist in response_json["items"]:
            if playlist['name'] == search_name:
                playlist_uri = playlist['uri']
                break

        return playlist_uri

    def get_spotify_uri(self, song_name, artist=""):
        # Able to change to dynamic form?

        """Search For the Song"""
        if artist == "":
            query = "https://api.spotify.com/v1/search?q={}&type=track&market=TW&limit=20&offset=0".format(
                song_name

            )
        else:
            query = "https://api.spotify.com/v1/search?q={}%2C{}&type=track%2Cartist&market=TW&limit=20&offset=0".format(
                song_name,
                artist
            )
        # query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
        #     song_name,
        #     artist
        # )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()
        # thinking how to handle refresh token how to check before run

        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri


def main():
    spotify_op = Spotify_Operation()
    print(spotify_op.token_is_expired())
    if spotify_op.token_is_expired() == False:
        pass
    print(spotify_op.token_is_expired())
    spotify_op.refresh_token()
    print(spotify_op.read_token())
    song_id = spotify_op.get_spotify_uri("Love in the First Degree ", "Bananarama")
    spotify_op.get_song_from_platlist("6hf5ZoJnNOf1VOStLAdfgf")
    playlist_id = spotify_op.get_playlist_id(spotify_user_id)

    song_in_the_playlist = [spotify_op.get_playlists_items(
        playlist_id.split(':')[2] if 'playlist' in playlist_id else 'nothing'
    )]
    spotify_op.add_song_to_playlist(
        song_id,
        playlist_id.split(':')[2] if 'playlist' in playlist_id else 'nothing'
    )


if __name__ == '__main__':
    main()
