"""
Containes the utility methods required.
"""


def extract_movie_id(link):
    """
    Get movie Id form movie url
    """
    return link.split('/')[-1]


def format_movie_data(movies, peoples):
    """
    Add the poeple on movies and formate the result.

    Arguments:
    movies: list of dectionaries thats represents the movie objects
    peoples: list of dectionaries thats represenst the people objects

    Return:
    data: list of dictonaries thats cotains formated movie data with people
    """
    data = list()
    movie_people = dict()
    for people in peoples:
        for film in people['films']:
            movie_id = extract_movie_id(film)
            movies_list = movie_people.get(movie_id, list())
            if people not in movies_list:
                movies_list.append(people)
            movie_people[movie_id] = movies_list
    for movie in movies:
        movie['people'] = movie_people.get(movie['id'], list())
        data.append(movie)
    return data
