# backend/main.py
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Movie API")

# CORS ‒ allow all origins for simplicity (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_PATH = "movies.db"


def get_db_connection():
    """
    Helper: opens a new SQLite connection.
    (Note: In production you might use a connection pool or an ORM.)
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # so we can access columns by name
    return conn


# --------------- Pydantic models ---------------

class MovieIn(BaseModel):
    title: str = Field(..., example="Inception")
    year: int = Field(..., example=2010)


class MovieOut(MovieIn):
    id: int = Field(..., example=1)


# --------------- Database initialization ---------------

@app.on_event("startup")
def startup_event():
    """
    Ensure that the database and 'movies' table exist on startup.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER NOT NULL
    );
    """)
    conn.commit()
    conn.close()


# --------------- CRUD Endpoints ---------------

@app.get("/movies", response_model=List[MovieOut])
def read_movies():
    """
    Return the list of all movies.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, year FROM movies ORDER BY id ASC;")
    rows = c.fetchall()
    conn.close()
    return [MovieOut(**row) for row in rows]


@app.get("/movies/{movie_id}", response_model=MovieOut)
def read_movie(movie_id: int):
    """
    Return a single movie by its ID.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, year FROM movies WHERE id = ?;", (movie_id,))
    row = c.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieOut(**row)


@app.post("/movies", response_model=MovieOut, status_code=201)
def create_movie(movie: MovieIn):
    """
    Create a new movie. Body: { "title": "...", "year": 20XX }
    Returns the created movie, including its new ID.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO movies (title, year) VALUES (?, ?);",
        (movie.title, movie.year),
    )
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return MovieOut(id=new_id, title=movie.title, year=movie.year)


@app.put("/movies/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: int, movie: MovieIn):
    """
    Update an existing movie by ID with a new title/year.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM movies WHERE id = ?;", (movie_id,))
    existing = c.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Movie not found")

    c.execute(
        "UPDATE movies SET title = ?, year = ? WHERE id = ?;",
        (movie.title, movie.year, movie_id),
    )
    conn.commit()
    conn.close()
    return MovieOut(id=movie_id, title=movie.title, year=movie.year)


@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int):
    """
    Delete a movie by ID. Returns HTTP 204 No Content on success.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM movies WHERE id = ?;", (movie_id,))
    existing = c.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Movie not found")

    c.execute("DELETE FROM movies WHERE id = ?;", (movie_id,))
    conn.commit()
    conn.close()
    return None