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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song_dict = {
            'id': self.object.id,
            'title': self.object.title,
            'artist': self.object.artist,
        }
        context['song_dict'] = song_dict
        return context

from django.http import JsonResponse, HttpResponseNotAllowed

@login_required
def toggle_favorites(request, song_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], 'Invalid method')

    song = get_object_or_404(Song, pk=song_id)
    favorite = Favorite.objects.filter(user=request.user, song=song)
    if favorite.exists():
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    else:
        Favorite.objects.create(user=request.user, song=song)
        return JsonResponse({'status': 'added'})

    
def search(request):
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(title__icontains=query)
        results = [{'id': song.id, 'title': song.title, 'artist': song.artist} for song in songs]#we need to fix this
    else:
        results = []
    return JsonResponse(results, safe=False)

def search_page(request):
    return render(request, 'rankings/search.html')

