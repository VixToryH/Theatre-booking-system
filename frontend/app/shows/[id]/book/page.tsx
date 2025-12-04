import SeatsGrid from "./SeatsGrid"

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

export default async function SeatsPage(props: any) {
  const params = await props.params;     

  const id = params.id;

  const show = await getShow(id);
  const seats = await getSeats(id);
  

  return (
    <main className="relative min-h-screen text-white">
      <div
        className="absolute inset-0 bg-cover bg-center -z-10"
        style={{
          backgroundImage: "url('/961b7b0dc1b53ba44323412c167ee9f6.jpg')",
        }}
      />
      <div className="absolute inset-0 bg-black/40 backdrop-blur-[3px] -z-10" />

      <div className="pt-16 text-center">
        <h1 className="text-5xl font-extrabold text-white drop-shadow-2xl">
          {show.title}
        </h1>

        <p className="mt-3 text-xl text-gray-200 opacity-90 drop-shadow">
          Оберіть найкращі місця у залі
        </p>
      </div>

      <SeatsGrid showId={id} seats={seats} />
    </main>
  );
}
