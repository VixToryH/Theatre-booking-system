"use client";

import { useEffect, useState } from "react";

export default function SimilarShows({ id }: { id: string }) {
  const [shows, setShows] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) return;

    fetch(`http://127.0.0.1:8000/api/recommendations/similar/${id}/`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => setShows(data.similar || []));
  }, [id]);

  if (shows.length === 0) return null;

  return (
    <div className="mt-16 text-white">
      <h2 className="text-2xl font-bold mb-4">Схожі вистави</h2>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {shows.map((show: any) => (
          <a
            href={`/shows/${show.id}`}
            key={show.id}
            className="bg-black/40 p-3 rounded-xl hover:bg-black/60 transition"
          >
            <div className="text-lg font-semibold">{show.title}</div>
          </a>
        ))}
      </div>
    </div>
  );
}
