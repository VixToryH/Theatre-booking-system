async function getSeats(showId: string) {
  const res = await fetch(`http://127.0.0.1:8000/api/shows/${showId}/seats/`, {
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Failed to load seats");
  return res.json();
}

async function getShow(showId: string) {
  const res = await fetch(`http://127.0.0.1:8000/api/shows/${showId}/`, {
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Failed to load show");
  return res.json();
}

export default async function SeatsPage({
  params,
}: {
  params: { id: string }; 
}) {
  const { id } = await params; 

  const show = await getShow(id);
  const seats = await getSeats(id);

  const rowsMap: Record<number, any[]> = {};

  seats.forEach((seat) => {
    if (!rowsMap[seat.row]) rowsMap[seat.row] = [];
    rowsMap[seat.row].push(seat);
  });

  const rows = Object.keys(rowsMap).length;
  const cols = rowsMap[1].length;

  return (
    <main className="relative min-h-screen text-white">
      {/* Фон */}
      <div
        className="absolute inset-0 bg-cover bg-center -z-10"
        style={{
          backgroundImage: "url('/961b7b0dc1b53ba44323412c167ee9f6.jpg')",
        }}
      />
      <div className="absolute inset-0 bg-black/40 backdrop-blur-[3px] -z-10" />

      {/* Назва вистави */}
      <div className="pt-16 text-center">
        <h1 className="text-5xl font-extrabold tracking-wide drop-shadow-2xl text-white">
          {show.title}
        </h1>

        <p className="mt-3 text-xl text-gray-200 opacity-90 drop-shadow">
          Оберіть найкращі місця у залі
        </p>
      </div>
                  {/* Схема залу */}
      <div className="flex justify-center mt-10">
        <div className="bg-black/40 backdrop-blur-md p-8 rounded-2xl shadow-xl space-y-3">

          {Object.values(rowsMap).map((rowSeats: any[], i) => (
            <div
              key={i}
              className="grid gap-3"
              style={{ gridTemplateColumns: `repeat(${cols}, 45px)` }}
            >
              {rowSeats.map((seat) => (
                <div key={seat.id} className="relative">

                  <div
                    className={`
                      w-[45px] h-[45px] rounded-lg flex items-center justify-center 
                      text-white text-sm font-semibold transition-all duration-150
                      ${
                        seat.is_taken
                          ? "bg-gray-600 cursor-not-allowed"
                          : seat.is_vip
                          ? "bg-yellow-500 hover:bg-yellow-400 hover:scale-105"
                          : "bg-green-600 hover:bg-green-500 hover:scale-105"
                      }
                    `}
                  >
                    {seat.row}.{seat.number}
                  </div>

                </div>
              ))}
            </div>
          ))}

        </div>
      </div>

      {/* Додатково*/}
      <div className="flex justify-center mt-6">
        <div className="flex gap-6 text-sm text-gray-200">
          <div className="flex items-center gap-2">
            <span className="w-4 h-4 rounded bg-green-600"></span> Вільні
          </div>
          <div className="flex items-center gap-2">
            <span className="w-4 h-4 rounded bg-yellow-500"></span> VIP
          </div>
          <div className="flex items-center gap-2">
            <span className="w-4 h-4 rounded bg-gray-600"></span> Зайняті
          </div>
        </div>
      </div>

    </main>
  );
}
