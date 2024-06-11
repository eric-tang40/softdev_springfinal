from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Song, Favorite, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.urls import reverse
import subprocess
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from .initialize2 import update
from .initialize1 import process_song_data



@login_required
def song_list(request):
    date_str = request.GET.get('date')
    if date_str:
        date = parse_date(date_str)
        songs = Song.objects.filter(chart_date=date).order_by('rank')
    else:
        date = parse_date('2024-06-05')
        songs = Song.objects.filter(chart_date=date).order_by('rank')

    return render(request, 'rankings/song_list.html', {'songs': songs})

@login_required
def update_songs(request):
    date_str = request.GET.get('date')
    action = request.GET.get('action')

    redirect_url = reverse('rankings:song_list')
    if date_str:
        redirect_url += f"?date={date_str}"

    if action == 'filter':
        return redirect(redirect_url)
    elif action == 'fetch' and date_str:
        try:
            process_song_data(date_str)
        except Exception as e:
            messages.error(request, f'Error updating songs data: {str(e)}')
    else:
        messages.error(request, "Please select a valid date to fetch data.")
    
    return redirect(redirect_url)

import matplotlib.pyplot as plt
from io import BytesIO
import base64
class SongDetailView(LoginRequiredMixin, DetailView):
    model = Song
    template_name = 'rankings/song_detail.html'
    context_object_name = 'song'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update()
        favorite = Favorite.objects.filter(user=self.request.user, song__title=self.object.title)
        if favorite.exists():
            is_favorite = 1
        else:
            is_favorite = 0
        song_dict = {
            'id': self.object.id,
            'title': self.object.title,
            'artist': self.object.artist,
            'album_name': self.object.album_name,
            'label': self.object.label,
            'favorite': is_favorite,
        }
        context['song_dict'] = song_dict
        
        song_entries = Song.objects.filter(title=self.object.title, artist=self.object.artist).order_by('chart_date')
        dates = [song.chart_date for song in song_entries]
        ranks = [song.rank for song in song_entries]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, ranks)
        plt.gca().invert_yaxis()
        plt.title(f"Billboard History for {self.object.title}")
        plt.xlabel('Date')
        plt.ylabel('Billboard Rank')
        plt.grid(True)
        plt.xticks(rotation=45)
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        context['chart_image'] = image_base64
        
        return context


@login_required
def toggle_favorites(request, song_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], 'Invalid method')

    song = get_object_or_404(Song, pk=song_id)
    favorite = Favorite.objects.filter(user=request.user, song__title=song.title)
    redirect_to_favorites = request.POST.get('redirect_to_favorites', False)
    
    if favorite.exists():
        favorite.delete()
        if redirect_to_favorites:
            return redirect('rankings:favorites')
        return JsonResponse({'status': 'removed'})
    else:
        Favorite.objects.create(user=request.user, song=song)
        return JsonResponse({'status': 'added'})

class SearchView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'rankings/search.html'
    context_object_name = 'songs'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Song.objects.filter(title__icontains=query).distinct('title')
        return Song.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'rankings/favorites.html'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('added_date')

class ArtistView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'rankings/artists.html'
    context_object_name = 'songs'

    def get_queryset(self):
        char = self.request.GET.get('c', '')
        if char: 
            return Song.objects.filter(artist__icontains=char).distinct('title')
        else:
            return Song.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['char'] = self.request.GET.get('c', '')
        return context


def data_analysis(request):
    return render(request, 'rankings/data_analysis.html')
