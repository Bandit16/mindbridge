from django.urls import path
from api.views import AlphabetImagesAPI

urlpatterns = [
    path('api/alphabet-images/<str:letter>/', AlphabetImagesAPI.as_view(), name='alphabet-images'),
]