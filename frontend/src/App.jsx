import { useEffect, useState } from "react";

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    // Fetch movies from the backend API
    fetch(import.meta.env.VITE_API_URL + "/movies")
      .then(res => res.json())
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