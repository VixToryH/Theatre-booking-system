import Link from "next/link";

async function getShows() {
  const res = await fetch("http://127.0.0.1:8000/api/shows/", {
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
    <main className="relative min-h-screen text-white">

      {/* Background image */}
<div
  className="absolute inset-0 bg-cover bg-center"
  style={{
    backgroundImage: "url('/961b7b0dc1b53ba44323412c167ee9f6.jpg')",
  }}
></div>

{/* Soft blur layer */}
<div className="absolute inset-0 backdrop-blur-sm"></div>

{/* Light dark overlay */}
<div className="absolute inset-0 bg-black/30"></div>

      

      {/* CONTENT ABOVE BACKGROUND */}
      <div className="relative z-10">

        {/* Header banner */}
        <section className="w-full h-[350px] flex flex-col justify-center items-center text-center">
          <h1 className="text-5xl font-extrabold drop-shadow-lg">
            Вистави театру
          </h1>
          <p className="text-lg mt-3 text-gray-300 max-w-2xl">
            Оберіть виставу, що подарує вам нові емоції та враження.
          </p>
        </section>

        {/* Shows grid */}
        <section className="max-w-6xl mx-auto py-12 px-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-10">
          {shows.map((show: any) => (
            <Link
              key={show.id}
              href={`/shows/${show.id}`}
              className="bg-[#1a1717]/80 backdrop-blur-md rounded-xl p-6 shadow-lg shadow-black/40 hover:scale-[1.03] transition transform duration-300 cursor-pointer"
            >
              <h2 className="text-2xl font-semibold">{show.title}</h2>
              <p className="text-gray-400 mt-2">
                {show.genres.map((g: any) => g.name).join(", ")}
              </p>

              <div className="mt-4 text-gray-300">
                <p><span className="font-semibold">Дата:</span> {show.date}</p>
                <p><span className="font-semibold">Тривалість:</span> {show.duration} хв</p>
                <p><span className="font-semibold">Ціна:</span> {show.price} грн</p>
              </div>

              <button className="mt-5 w-full py-2 bg-white text-black rounded-lg font-semibold hover:bg-gray-200 transition">
                Переглянути
              </button>
            </Link>
          ))}
        </section>
      </div>
    </main>
  );
}

