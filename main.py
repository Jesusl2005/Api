from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = 'Mi aplicacion con FastAPI'
app.version = '0.0.1'

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_Length=5,max_Length=15)
    overview: str = Field(min_Length=15, max_Length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_Length=5, max_Length=15)

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'Mi pelicula',
                'overview': 'Descripcion de la pelicula',
                'year': 2022,
                'rating': 9.8,
                'category': 'Accion'
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Accion'
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        'year': 2010,
        'rating': 7.8,
        'category': 'Accion'
    }
]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')


@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item['id'] == id:
            return item
    return []

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_Length=5, max_Length=15)):
    return [item for item in movies if item['category'] == category]

@app.post('/movies', tags=['Movies'])
def create_movies(movie: Movie):
    movies.append(movie)
    return movies

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies

    

