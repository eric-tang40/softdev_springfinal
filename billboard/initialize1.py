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
api_key = settings.API_KEY

conn = http.client.HTTPSConnection("billboard-api2.p.rapidapi.com")

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': "billboard-api2.p.rapidapi.com"
}

from django.utils.dateparse import parse_date

def process_song_data(date):
    conn.request("GET", f"/hot-100?date={date}&range=1-100", headers=headers) # Placeholder date

    res = conn.getresponse()
    data = res.read()

    songs = (data.decode("utf-8"))
    songs_data = json.loads(songs)
    song_list = songs_data.get('content', [])
    
    for song_key, song_info in song_list.items():
        title = song_info.get('title')
        artist = song_info.get('artist')
        rank = int(song_info.get('rank'))
        peak_position = int(song_info.get('peak position'))
        weeks_on_chart = int(song_info.get('weeks on chart'))

        chart_date = parse_date(date)  # Placeholder date

        song, created = Song.objects.update_or_create(
            title=title,
            artist=artist,
            chart_date=chart_date,
            defaults={
                'rank': rank,
                'album_name': '',
                'peak_position': peak_position,
                'weeks_on_chart': weeks_on_chart,
                'label': '',
                'genre': ''
            }
        )
        if created:
            print(f"Added new song: {title} by {artist}")
        else:
            print(f"Updated song: {title} by {artist}")
            
import asyncio
import sys
async def main():
    if len(sys.argv) == 2:
        date = sys.argv[1]
        process_song_data(date)

if __name__ == "__main__":
    asyncio.run(main())

