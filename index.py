from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

# Schemas
class Movie(BaseModel):
    id: Optional[int] = None
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
def create_movie(moviedto: Movie):
    movies.append(dict(moviedto))
    return movies

@app.put('/movies/{movie_id}', tags=["movies"])
def update_movie(movie_id: int, moviedto: Movie):
    movie_index = None
    for idx, movie in enumerate(movies):
        if movie['id'] == movie_id:
            movie_index = idx
            break
    
    if movie_index is not None:
        movies[movie_index]['title'] = moviedto.title
        movies[movie_index]['overview'] = moviedto.overview
        movies[movie_index]['year'] = moviedto.year
        movies[movie_index]['rating'] = moviedto.rating
        movies[movie_index]['category'] = moviedto.category
        return movies[movie_index]
    else:
        return {"error": "Movie not found"}


@app.delete('/movies/{movie_id}', tags=["movies"])
def delete_movie(movie_id: int):
    movie_index = None
    for idx, movie in enumerate(movies):
        if movie['id'] == movie_id:
            movie_index = idx
            break
    
    if movie_index is not None:
        deleted_movie = movies.pop(movie_index)
        return {"message": f"Movie with ID {movie_id} deleted", "deleted_movie": deleted_movie}
    else:
        return {"error": "Movie not found"}

