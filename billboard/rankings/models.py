from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    rank = models.IntegerField()
    chart_date = models.DateField()
    album_name = models.CharField(max_length=255, blank=True, null=True)
    peak_position = models.IntegerField(blank=True, null=True)
    weeks_on_chart = models.IntegerField(blank=True, null=None)
    label = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        
    def __str__(self):
        return f"{self.user.username} - {self.song.title}"
