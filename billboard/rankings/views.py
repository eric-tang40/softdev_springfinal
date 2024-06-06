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

