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
    
def search(request):
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(title__icontains=query)
        results = [{'id': song.id, 'title': song.title, 'artist': song.artist} for song in songs]
    else:
        results = []
    return JsonResponse(results, safe=False)

def search_page(request):
    return render(request, 'search.html')