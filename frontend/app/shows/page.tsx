import Link from "next/link";

async function getShows() {
  const res = await fetch("http://127.0.0.1:8000/api/shows/api/", {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to load shows");
  }

  return res.json();
}

export default async function ShowsPage() {
  const shows = await getShows();

  return (
    <main style={{ padding: "20px" }}>
      <h1>Список вистав:</h1>

      <ul>
        {shows.map((show: any) => (
          <li key={show.id}>
            <Link href={`/shows/${show.id}`}>
              <strong>{show.title}</strong>
            </Link>
            <br />
            Жанри: {show.genres.map((g: any) => g.name).join(", ")}
          </li>
        ))}
      </ul>
    </main>
  );
}
