import os
os.chdir("..")

import django
# In case that we need it later
#from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billboard.settings')
# We need to enable the following because jupyter is running an async loop
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import json
import http.client
from rankings.models import Song

from django.conf import settings
import http.client


def process_song_data(song):
    api_key = settings.API_KEY
    conn = http.client.HTTPSConnection("spotify23.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "spotify23.p.rapidapi.com"
    }
    if not song.album_name or not song.label:
        query = f"{song.title} {song.artist}".replace(" ", "%20")
        conn.request("GET", f"/search/?q={query}&type=tracks", headers=headers)
        res = conn.getresponse()
        data = res.read()
        songs_data = json.loads(data.decode("utf-8"))

        items = songs_data.get('tracks', {}).get('items', [])
        if items:
            first_item = items[0].get('data', {})
            album_info = first_item.get('albumOfTrack', {})
            album_name = album_info.get('name', '')
            label = first_item.get('contentRating', {}).get('label', '')
            song.album_name = album_name
            song.label = label
    song.save()

def update():
    for song in Song.objects.all():
        process_song_data(song)

if __name__ == "__main__":
    update()
