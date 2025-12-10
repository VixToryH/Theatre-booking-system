"use client";

import { useEffect, useState } from "react";

export default function RecommendedShows() {
  const [shows, setShows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) return;

    fetch("http://127.0.0.1:8000/api/recommendations/", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => {
        setShows(data.recommendations || []);
        setLoading(false);
      });
  }, []);

  if (loading) return null;
  if (shows.length === 0) return null;

  return (
    <div className="mt-16 text-white max-w-5xl mx-auto px-6">
      <h2 className="text-3xl font-bold mb-5">Рекомендовано для вас</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {shows.map((show: any) => (
          <a
            href={`/shows/${show.id}`}
            key={show.id}
            className="bg-black/40 p-4 rounded-xl backdrop-blur-sm hover:bg-black/60 transition shadow-lg"
          >
            <div className="text-xl font-semibold">{show.title}</div>
            <p className="text-gray-300 mt-2">{show.description?.slice(0, 80)}...</p>
          </a>
        ))}
      </div>
    </div>
  );
}
