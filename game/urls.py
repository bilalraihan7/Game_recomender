# game_recommendation_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_games, name='recommend_games'),
]
