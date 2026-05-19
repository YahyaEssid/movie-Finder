import anthropic
import requests
import os
from num2words import num2words
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

def getUserInput():
    return input("describe what kind of movie you like to watch: ")


def getRecommendationsFromClaude(userInput):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role":"user",
                "content": userInput
            }
        ],
        system = "System: You are a movie expert. Given a user's preference, return exactly 5 movie recommendation only 5, return just the title of each movie seperated by a coma ',' and nothing else"

    )
    return message.content[0].text.split(",")


def fetchMovieDetails(movies):
     movie_data = []
     headers = {
        "Authorization":f"Bearer {os.environ.get('TMDB_API_TOKEN')}"
    }
     for movie in movies:
        params = {
        "query": movie
        }
        response = requests.get('https://api.themoviedb.org/3/search/movie?', headers=headers, params=params)
        movie_data.append(response.json()["results"][0])
     return movie_data

def renderMovieCards(movie_data):
   i = 1
   for movie in movie_data:
       print(f"{num2words(i, to = 'ordinal')} recommendation: {movie["title"]}")
       i += 1

def main():
    description = getUserInput()
    recommendation = getRecommendationsFromClaude(description)
    details = fetchMovieDetails(recommendation)
    renderMovieCards(details)

main()