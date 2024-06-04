from django.urls import path
from . import views

app_name = 'rankings'

urlpatterns = [
    path("songs/", views.song_list, name="song_list"),
    path("songs/<int:pk>/", views.SongDetailView.as_view(), name="song_detail"),
    path('songs/<int:pk>/toggle_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('search/', views.search, name='search')
    ]
