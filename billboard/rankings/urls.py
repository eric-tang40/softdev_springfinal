from django.urls import path
from .views import get_billboard_data

app_name = 'rankings'

urlpatterns = [
    path('', get_billboard_data, name='get_billboard_data'), 
]
