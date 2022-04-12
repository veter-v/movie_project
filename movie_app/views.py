from django.shortcuts import render, get_object_or_404
from .models import Movie, Director, Actor
from django.db.models import F, Sum, Max, Min, Avg, Count, Value


# Create your views here.

def show_one_actor(request, slug_actor: str):
    actor = get_object_or_404(Actor, slug=slug_actor)
    return render(request, 'movie_app/one_actor.html', {'actor': actor})


def show_all_actors(request):
    actors = Actor.objects.order_by('last_name', 'first_name')
    # for director in directors:
    #     director.save()
    return render(request, 'movie_app/actors.html', {'actors': actors})


def show_one_director(request, slug_director: str):
    director = get_object_or_404(Director, slug=slug_director)
    return render(request, 'movie_app/one_director.html', {'director': director})


def show_all_directors(request):
    directors = Director.objects.order_by('last_name', 'first_name')
    # for director in directors:
    #     director.save()
    return render(request, 'movie_app/directors.html', {'directors': directors})


def show_all_movies(request):
    # movies = Movie.objects.order_by(F('year').desc(nulls_first=True), 'rating')
    movies = Movie.objects.annotate(true_bool=Value(True),
                                    false_bool=Value(False),
                                    str_field=Value('hello'),
                                    int_field=Value(123),
                                    new_budget=F('budget')+100,
                                    budget_plus_year=F('budget') + F('year'),
                                    )
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    # for movie in movies:
    #     movie.save()  для простановки всех slug в БД
    return render(request, 'movie_app/all_movies.html', {'movies': movies, 'agg': agg})


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {'movie': movie})
