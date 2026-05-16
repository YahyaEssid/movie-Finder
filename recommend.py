import anthropic
import requests
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
def extract_keywords():
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role":"user",
                "content":f"{input("what kind of movie you like to watch:")}"
            }
        ],
        system = "based on teh description the user will input i need you to reccommend a movie. i want you to return the output with a certain format" \
        "I want to just return names of movie seprated by space nothing else no introduction no ending no numbering nothing. just names of movie seperated by a coma that's it" \
        "it's very important that the names are sperated by commas like for example movie 1, movie 2, and so on"

    )
    return(message.content[0].text.split(","))


def find_movies(movies):
    list_of_movies = []
    headers = {
        "Authorization":f"Bearer {os.environ.get('TMDB_API_TOKEN')}"
    }
    for movie in movies:
        params = {
        "query":movie
        }
        response = requests.get('https://api.themoviedb.org/3/search/movie?', headers=headers, params=params)
        list_of_movies.append(response.json()["results"])
    return(list_of_movies)


def extract_movies(movies):
    titles=[]
    for movie_list in movies:
        for movie_dict in movie_list:
            titles.append(movie_dict.get('title'))
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role":"user",
                "content":titles
            }
        ],
        system = "you are givinhg a movie title along with "
    )

extract_movies(find_movies(extract_keywords()))
