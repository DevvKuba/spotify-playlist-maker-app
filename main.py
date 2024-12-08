import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

REDIRECT_URL = "http://example.com"


SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET,
                                       redirect_uri=REDIRECT_URL,
                                       scope="playlist-modify-private",
                                       show_dialog=True,
                                       cache_path="token.txt",
                                       username="Kuba",
                                       ))

user_id = spotify.current_user()["id"]


specific_date = str(input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "))
year = input("Confirm year ")


header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

date_url = f"https://www.billboard.com/charts/hot-100/{specific_date}/"

response = requests.get(url=date_url, headers=header)
top_songs = response.text

soup = BeautifulSoup(top_songs, "html.parser")
titles = soup.select("li ul li h3")

song_titles = [title.getText().strip() for title in titles]

song_uris=[]

for song in song_titles:
    uri_list = spotify.search(q=song, type="track", limit=1)

    try:
        uri = uri_list["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} isn't available on spotify :(")

playlist = spotify.user_playlist_create(user=user_id,
                             name=f"{specific_date} Billboard 100",
                             public=False,
                             collaborative=False,
                             description=f"Top 100 tracks from date: {specific_date}")

spotify.user_playlist_add_tracks(user=user_id,
                                 playlist_id=playlist["id"],
                                 tracks=song_uris,
                                 position=None)

