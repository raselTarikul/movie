from django.shortcuts import render
from django.template import Context
from django.views import View
from django.core.cache import cache
from movie.utils import format_movie_data
from movie.exceptions.api_exception import APIErrorException
from .client import GhibliClient

class MovieList(View):
    """
    Controller for Movie List
    """
    template_name = "film/movie_list.html"
    client = GhibliClient()

    def get(self, request, *args, **kwargs):
        """
        Responsible for resonse the get request for movie 
        list. Used django caching for caching data for one
        minuts.
        """
        formated_movies = cache.get('formated_movies')
        if not formated_movies:
            try:
                movies = self.client.get_movies()
                people = self.client.get_people()
                formated_movies = format_movie_data(movies, people)
                cache.set('formated_movies', formated_movies, 60)
            except APIErrorException as e:
                # should be logged value instead of print
                print(e)
                formated_movies = list()
        return render(request, self.template_name, {'movies': formated_movies})
