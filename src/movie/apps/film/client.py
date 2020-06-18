import requests
from django.conf import settings
from movie.exceptions.api_exception import APIErrorException


class GhibliClient(object):
    """
    A wrapper class for making http request on Ghibli apis
    """

    def __init__(self):
        """
        Initialized the base url for Ghibli apis
        """
        self.base_url = settings.API_BASE_URL


    def _get_request(self, path):
        """
        Makes http get request on Ghibli apis

        Arguments:
        path: string path of the resource

        Returns:
        response: Response object from requests

        Exceptions: 
        Raise APIErrorException exception if the api request 
        does not success.
        """

        url = self.base_url + path
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        else:
            raise APIErrorException('Api Not working')

    def get_movies(self):
        """
        Make request on Movie List api, and return Movie List as Json. 
        """
        path = '/films/'
        response = self._get_request(path)
        return response.json()

    def get_people(self):
        """
         Make request on People List api, and return People List as Json.
        """
        path = '/people/'
        response = self._get_request(path)
        return response.json()