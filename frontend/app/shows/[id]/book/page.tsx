async function getSeats(showId: string) {
  const res = await fetch(`http://127.0.0.1:8000/api/shows/${showId}/seats/`, {
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Failed to fetch seats");

  return res.json();
}

export default async function SeatsPage(props: { params: Promise<{ id: string }> }) {
  const { id } = await props.params;
  const seats = await getSeats(id);

  return (
    <main style={{ padding: 20 }}>
      <h1>Вибір місця</h1>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(10, 40px)",
        gap: "8px",
        marginTop: "20px",
      }}>
        {seats.map((seat: any) => (
          <div
            key={seat.id}
            style={{
              width: 40,
              height: 40,
              borderRadius: 6,
              background: seat.is_taken
                ? "#777"
                : seat.is_vip
                ? "#e5b400"
                : "#1e90ff",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "white",
              cursor: seat.is_taken ? "not-allowed" : "pointer",
            }}
          >
            {seat.number}
          </div>
        ))}
      </div>
    </main>
  );
}
