from django.urls import path
from api.views import *

urlpatterns = [
    path('api/alphabet-images/<str:letter>/', AlphabetImagesAPI.as_view(), name='alphabet-images'),
    path('api/game-images/<str:letter>/',GameImagesAPI.as_view(),name='game-images') ,
    path('test-firebase/', test_firebase, name='test-firebase'),
    path('sync-users/', SyncFirebaseUsers.as_view(), name='sync-users'),
]