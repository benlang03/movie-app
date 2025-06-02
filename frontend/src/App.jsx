import { useEffect, useState } from "react";

function App() {
  const [movies, setMovies] = useState([]);

  const BACKEND = import.meta.env.VITE_BACKEND_URL;

  useEffect(() => {
    // Fetch movies from the backend API
    fetch("https://movie-app-production-0f0c.up.railway.app/movies")
      .then(res => {
        if (!res.ok) throw new Error("Status " + res.status);
        return res.json();
      })
      .then(data => setMovies(data))
      .catch(err => console.error("Failed to fetch movies:", err));
  }, []);

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">🎬 Movie Listings</h1>
      <ul>
        {movies.map(movie => (
          <li key={movie.id} className="border-b py-2">
            <h2 className="text-xl font-semibold">{movie.title}</h2>
            <p className="text-sm text-gray-700">{movie.year}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;