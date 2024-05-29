from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.urls import reverse
import requests


def get_billboard_data():
    billboard_API = f"https://rapidapi.com/LDVIN/api/billboard-api/playground/apiendpoint_5ed3a90f-9e50-4b1a-b2bd-f5129f7f6695"
    response = requests.get(billboard_API)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        print("test")
        return data
    else:
        return None
# Create your views here.
