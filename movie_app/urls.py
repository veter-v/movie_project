from . import views
from django.urls import path

urlpatterns = [
    path('', views.show_all_movies),
    path('movie/<slug:slug_movie>/', views.show_one_movie, name='movie-detail'),
    path('directors/', views.show_all_directors),
    path('directors/<slug:slug_director>/', views.show_one_director, name='director-detail'),
    path('actors/', views.show_all_actors),
    path('actors/<slug:slug_actor>', views.show_one_actor, name='actor-detail'),
]