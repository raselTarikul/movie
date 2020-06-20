from unittest import mock
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from movie.apps.film.client import GhibliClient
from movie.exceptions.api_exception import APIErrorException
from movie.utils import extract_movie_id, format_movie_data

class MockResponse(object):
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

class TestGhibliClient(TestCase):
    def setUp(self):
        self.chilib_client = GhibliClient()

    @mock.patch('movie.apps.film.client.GhibliClient._get_request')
    def test_movie_api_success(self, mock_get_request):
        mock_get_request.return_value = MockResponse(
            [{'id': 1, 'teile': 'Test 1'}, {'id': 2, 'teile': 'Test 2'}], 200)
        movie = self.chilib_client.get_movies()
        self.assertEqual(len(movie), 2)

    @mock.patch('movie.apps.film.client.requests.get')
    def test_movie_api_error(self, mock_request):
        mock_request.return_value = MockResponse({}, 504)
        self.assertRaises(APIErrorException, self.chilib_client.get_movies)

    @mock.patch('movie.apps.film.client.GhibliClient._get_request')
    def test_people_api_success(self, mock_get_request):
        mock_get_request.return_value = MockResponse(
            [{'id': 1, 'name': 'Test 1'}, {'id': 2, 'name': 'Test 2'}], 200)
        people = self.chilib_client.get_people()
        self.assertEqual(len(people), 2)

    @mock.patch('movie.apps.film.client.requests.get')
    def test_people_api_error(self, mock_request):
        mock_request.return_value = MockResponse({}, 504)
        self.assertRaises(APIErrorException, self.chilib_client.get_people)
    

class TestUtils(TestCase):
    def setUp(self):
        self.movies = [{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '4'}]
        self.people = [
            {'id': '1', 'films': ['https://ghibliapi.herokuapp.com/films/1']}, 
            {'id': '2', 'films': ['https://ghibliapi.herokuapp.com/films/1']}, 
            {'id': '3', 'films': ['https://ghibliapi.herokuapp.com/films/3']}, 
            {'id': '4', 'films': ['https://ghibliapi.herokuapp.com/films/4']}
            ]
    def test_extract_movie_id(self):
        movie_url = 'https://ghibliapi.herokuapp.com/films/030555b3-4c92-4fce-93fb-e70c3ae3df8b'
        movie_id = extract_movie_id(movie_url)
        self.assertEqual(movie_id, '030555b3-4c92-4fce-93fb-e70c3ae3df8b')

    def test_format_movie_data(self):
        formated_data = format_movie_data(self.movies, self.people)
        self.assertEqual(len(formated_data[0]['people']), 2)
        self.assertEqual(len(formated_data[1]['people']), 0)
        self.assertEqual(len(formated_data[2]['people']), 1)
        self.assertEqual(len(formated_data[3]['people']), 1)


class TestMovieList(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('movie-list')
        self.movies = [
            {'id': '1', 'title': 'Title 1'}, 
            {'id': '2', 'title': 'Title 2'}, 
            {'id': '3', 'title': 'Title 3'}, 
            {'id': '4', 'title': 'Title 4'},
            {'id': '5', 'title': 'Title 5'}]

        self.movies_cache = [
            {'id': '1', 'title': 'Title 1'}, 
            {'id': '2', 'title': 'Title 2'}, 
            {'id': '3', 'title': 'Title 3'}, 
            {'id': '4', 'title': 'Title 4'}]
        self.people = [
            {'id': '1', 'name': 'Name 1', 'films': ['https://ghibliapi.herokuapp.com/films/1']}, 
            {'id': '2', 'name': 'Name 2', 'films': ['https://ghibliapi.herokuapp.com/films/1']}, 
            {'id': '3', 'name': 'Name 3', 'films': ['https://ghibliapi.herokuapp.com/films/3']}, 
            {'id': '4', 'name': 'Name 4', 'films': ['https://ghibliapi.herokuapp.com/films/4']}
            ]
    
    @mock.patch('movie.apps.film.client.GhibliClient.get_movies')
    @mock.patch('movie.apps.film.client.GhibliClient.get_people')
    def test_view(self, mock_get_people, mock_get_movies):
        mock_get_movies.return_value = self.movies
        mock_get_people.return_value = self.people
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['movies']), 5)

    @mock.patch('movie.apps.film.views.cache.get')
    @mock.patch('movie.apps.film.client.GhibliClient.get_movies')
    @mock.patch('movie.apps.film.client.GhibliClient.get_people')
    def test_cache(self, mock_get_people, mock_get_movies, mock_cache_get):
        mock_get_movies.return_value = self.movies
        mock_get_people.return_value = self.people
        mock_cache_get.return_value = self.movies_cache
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['movies']), 4)
