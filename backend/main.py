# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Movie API")

# Allow CORS for local dev (React dev server) and all origins for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, specify your frontend domain instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample movie data (could also load from a JSON file or database)
movies = [
    {"id": 1, "title": "The Matrix", "year": 1999},
    {"id": 2, "title": "Inception", "year": 2010},
    {"id": 3, "title": "Interstellar", "year": 2014}
]

@app.get("/movies")
def get_movies():
    """Return the list of movies."""
    return movies