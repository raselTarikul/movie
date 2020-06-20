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
        formated_data = cache.get('formated_data')
        if not formated_data:
            try:
                movies = self.client.get_movies()
                people = self.client.get_people()
                formated_data = format_movie_data(movies, people)
                cache.set('formated_data', formated_data, 60)
            except APIErrorException as e:
                # should be logged value instead of print
                print(e)
                formated_data = list()
        return render(request, self.template_name, {'movies': formated_data})
