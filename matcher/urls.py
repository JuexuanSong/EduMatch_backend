from django.urls import path
from .views import get_matches

urlpatterns = [
    path('matches/', get_matches, name='get_matches'),
]
