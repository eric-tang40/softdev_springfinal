from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Song, Favorite, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import http.client
from django.conf import settings
from django.utils.dateparse import parse_date



@login_required
def song_list(request):
    songs = Song.objects.all().order_by('rank')
    return render(request, 'rankings/song_list.html', {'songs': songs})

class SongDetailView(LoginRequiredMixin, DetailView):
    model = Song
    template_name = 'rankings/song_detail.html'
    context_object_name = 'song'

@login_required
def add_to_favorites(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, song=song)
    if created:
        return JsonResponse({'status': 'added'})
    else:
        return JsonResponse({'status': 'not added'})

def fetch_and_display_songs(request):
    api_key = settings.API_KEY

    conn = http.client.HTTPSConnection("billboard-api2.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "billboard-api2.p.rapidapi.com"
    }

    conn.request("GET", "/hot-100?date=2019-05-11&range=1-100", headers=headers)  # Placeholder date

    res = conn.getresponse()
    data = res.read()

    songs = data.decode("utf-8")
    songs_data = json.loads(songs)
    print("API response:", songs_data)  # Add this line

    song_list = songs_data.get('content', [])
    print("Song list:", song_list)  # Add this line

    def process_song_data(songs_data):
        for song_info in songs_data:
            title = song_info.get('title')
            artist = song_info.get('artist')
            rank = int(song_info.get('rank'))
            peak_position = int(song_info.get('peak position'))
            weeks_on_chart = int(song_info.get('weeks on chart'))

            chart_date = parse_date('2019-05-11')  # Placeholder date

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

    process_song_data(song_list)

    # Fetch the songs from the database to pass to the template
    songs = Song.objects.filter(chart_date='2019-05-11')  # Use the same date as above
    print(f"Number of songs: {songs.count()}")  # Add this line

    return render(request, 'song_list.html', {'songs': songs})
