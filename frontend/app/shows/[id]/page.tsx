import SimilarShows from "./SimilarShows";
import RatingStars from "@/app/components/RatingStars";


async function getShow(id: string) {
  const res = await fetch(`http://127.0.0.1:8000/api/shows/${id}/`, {
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Failed to fetch show");

  return res.json();
}

export default async function ShowDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const show = await getShow(id);

  return (
    <main className="relative min-h-screen text-white flex flex-col items-center pt-32">

      {/* Фон */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('/961b7b0dc1b53ba44323412c167ee9f6.jpg')",
          filter: "blur(4px)",
          transform: "scale(1.05)",
        }}
      />
      <div className="absolute inset-0 bg-black/40" />

      {/* Контент */}
      <div className="relative z-10 w-full max-w-4xl px-6 text-center">
        
        {/* Заголовок */}
        <h1 className="text-5xl font-bold mb-10 drop-shadow-xl">{show.title}</h1>

        {/* Опис */}
        <p className="text-lg leading-relaxed max-w-3xl mx-auto mb-12 drop-shadow-lg">
          {show.description}
        </p>

        {/* Інформаційна картка */}
        <div className="mx-auto p-6 rounded-3xl w-fit text-center 
          bg-white/15 backdrop-blur-xl 
          border border-white/20 shadow-2xl"
        >
          <p><b>Дата:</b> {show.date}</p>
          <p><b>Час:</b> {show.time}</p>
          <p><b>Тривалість:</b> {show.duration} хв</p>
          <p><b>Ціна:</b> {show.price} грн</p>

          {show.genres?.length > 0 && (
            <p>
              <b>Жанри:</b> {show.genres.map((g: any) => g.name).join(", ")}
            </p>
          )}

          {show.hall && (
            <p>
              <b>Зала:</b> {show.hall.name}
            </p>
          )}

              <RatingStars showId={show.id} />
          
        </div>

        {/* Кнопка */}
        <a
          href={`/shows/${show.id}/book`}
          className="block mt-12 mx-auto bg-red-600 hover:bg-red-700 text-white py-4 px-10 rounded-2xl font-semibold shadow-xl transition w-fit"
        >
          Забронювати місце
        </a>
      </div>

      {/* СХОЖІ ВИСТАВИ */}
      <div className="relative z-10 w-full mt-20 px-6 max-w-5xl">
        <SimilarShows id={id} />
      </div>
      

    </main>
  );
}
