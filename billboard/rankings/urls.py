from django.urls import path
from . import views

app_name = 'rankings'

urlpatterns = [
    path("songs/", views.song_list, name="song_list"),
    path("songs/<int:pk>/", views.SongDetailView.as_view(), name="song_detail"),
    path('songs/<int:song_id>/toggle_favorites/', views.toggle_favorites, name='toggle_favorites'),
    path('search/', views.search, name='search'),
    ]
