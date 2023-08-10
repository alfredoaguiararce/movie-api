from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# The above class represents a movie with attributes such as id, title, overview, year, rating, and
# category.
class Movie(BaseModel):
    id: int
    title : str
    overview : str
    year: int
    rating: float
    category : str


app = FastAPI()
app.title = "FastApi app"
app.version = "0.0.1"

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Aventura'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 3,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Romance'    
    },
]


@app.get('/', tags=['home'])
def message():
    return {"hello": "world",}

@app.get('/html', tags=['home'])
def message_html():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

#  Path parameters
@app.get('/movies/{id}', tags=['movies'])
def get_movie_by_id(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    
    return None

# Query parameters
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return [item for item in movies if item["category"].lower() == category.lower()]

@app.post("/movies", tags=["movies"])
def create_movie(request: Request, moviedto: Movie):
    movies.append(dict(moviedto))
    return movies