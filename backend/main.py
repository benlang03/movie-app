from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Movie App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

movies = [
    {"id": 1, "title": "The Matrix", "year": 1999},
    {"id": 2, "title": "Inception", "year": 2010},
    {"id": 3, "title": "Interstellar", "year": 2014},
]

@app.get("/movies")
def get_movies():
    """Get all movies. """
    return movies