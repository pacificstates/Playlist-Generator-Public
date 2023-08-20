import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import *

CLIENT_ID = "REDACTED"
CLIENT_SECRET = "REDACTED"
REDIRECT_URL = "http://example.com"
date = input("What day would you like to travel to? Use the YYYY-MM-DD format: ")
url = "https://www.billboard.com/charts/hot-100/"

response = requests.get(url=f"{url}{date}/")
contents = response.text
soup = BeautifulSoup(contents, "html.parser")

song_titles = soup.select("li ul li h3")

top_100 = []

for song in song_titles:
    x = song.getText().strip()
    top_100.append(x)

print(top_100)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
)
user_id = sp.current_user()['id']
track_ids = []

for song in top_100:
    search_result = sp.search(q=song)
    track_ids.append(search_result['tracks']['items'][0]['id'])

print(track_ids)

playlist = sp.user_playlist_create(user_id, f"{date} Billboard 100", public=False, description=f"A playlist of the top "
                                                                                              f"100 Bilboard charts on "
                                                                                              f"{date}")
print(playlist)
sp.playlist_add_items(playlist["id"], track_ids)
