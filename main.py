from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

# Schemas
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid credentials")
        

class User(BaseModel):
    email: str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title : str = Field(default='Mi pelicula' ,min_length=5, max_length=15)
    overview : str = Field(default='Descripcion de la pelicula' ,min_length=15, max_length=50)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(default=9.8 ,le=10)
    category : str = Field(default='Categoria de la pelicula' ,min_length=15, max_length=50)

    class Config:
        schema_extra = {
            "Example" : {
                "id" : 1
                ,"title" : "Mi pelicula"
                ,"overview": "Descripcion de la pelicula"
                ,"year": 2022
                ,"rating": 9.8
                ,"category": "action"
            }
        }


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

@app.post('/login',tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        jwt: str = create_token(dict(user))
        return JSONResponse(status_code=200, content=jwt)
    else:
        return JSONResponse(status_code=404, content={"error": "Not valid user"})

@app.get('/', tags=['home'], response_model=dict, status_code=200)
def message()-> dict:
    dictionary = {"hello": "world",}
    return JSONResponse(status_code=200, content=dictionary)

@app.get('/html', tags=['home'])
def message_html():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

#  Path parameters
@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=1, le= 100)) -> Movie:
    movie_index = None
    for idx, movie in enumerate(movies):
        if movie['id'] == id:
            movie_index = idx
            break
    
    if movie_index is not None:
        return JSONResponse(movies[movie_index])
    else:
        return JSONResponse({"error": "Movie not found"})

# Query parameters
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [JSONResponse(content=item) for item in movies if item["category"].lower() == category.lower()]

@app.post("/movies", tags=["movies"], status_code=201)
def create_movie(moviedto: Movie):
    movies.append(dict(moviedto))
    return JSONResponse(status_code=201, content=movies)

@app.put('/movies/{movie_id}', tags=["movies"], status_code=200)
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


@app.delete('/movies/{movie_id}', tags=["movies"], status_code=200)
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



