# Movie Demo
This project is done on the response to the given task

### Solutions Approach
I have created a client, movie/src/movie/apps/film/client.py which is responsible for calling the 
movie and people APIs. The movie and people data are formatted and marges on a utils method on movie/src/movie/utils.py. format_movie_data data marges on O(m+n). 
Django Caching is used to cache the data for 1 min. When someone loads the page the first time it calls the APIs and cache data for 1 min, so for any request within 1 min will not call the APIs.

Advantages of this approach:
1. Only call the APIs when is needed, no additional API call.
2. Used loads the data second time and onwards will get data faster.

Disadvantages of this approach:
1. when calling for the first time the page load is slower

### Alternative Approach
Another way we can solve this problem is to save the data into a database and use a background task to sync the data with the APIs on every 1 minute.

Advantages of this approach:
1. Every page load will be faster as there is no API call on page load

Disadvantages of this approach:
1. It will create unnecessary API call even the time there is no user.


### Installation
Clone the project from git and follow the following steps

Build a docker image:

```
docker build -t movie .
```
Run the test cases.

```
docker run -it movie python /opt/app/src/manage.py test movie
```
The following project run the project on port 8000

```
docker run --rm -it -p 8000:8000 movie
```

