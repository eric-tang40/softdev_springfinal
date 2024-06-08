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

    if action == 'filter':
        return redirect(f"{reverse('rankings:song_list')}?date={date_str}")
    elif action == 'fetch' and date_str:
        try:
            result = subprocess.run(['python', 'initialize1.py', date_str], check=True, capture_output=True, text=True)
            if result.returncode == 0:
                messages.success(request, 'Songs data successfully fetched and updated for ' + date_str)
            else:
                messages.error(request, 'Failed to update songs data: ' + result.stderr)
        except subprocess.CalledProcessError as e:
            messages.error(request, f'Error updating songs data: {str(e)}')
        
        return redirect('rankings:song_list')
    else:
        messages.error(request, "Please select a valid date to fetch data.")
    
    return redirect('rankings:song_list')


class SongDetailView(LoginRequiredMixin, DetailView):
    model = Song
    template_name = 'rankings/song_detail.html'
    context_object_name = 'song'
    update()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        return context


@login_required
def toggle_favorites(request, song_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], 'Invalid method')

    song = get_object_or_404(Song, pk=song_id)
    favorite = Favorite.objects.filter(user=request.user, song__title=song.title)
    if favorite.exists():
        favorite.delete()
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