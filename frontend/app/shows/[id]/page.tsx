async function getShow(id: string) {
  const res = await fetch(`http://127.0.0.1:8000/api/shows/api/${id}/`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch show");
  }

  return res.json();
}

export default async function ShowPage(props: { params: Promise<{ id: string }> }) {
  const { id } = await props.params;   // ⬅️ ⬅️ ОБОВʼЯЗКОВО await !!

  const show = await getShow(id);

  return (
    <main style={{ padding: "20px" }}>
      <h1>{show.title}</h1>

      <p><strong>Опис:</strong> {show.description}</p>

      <p>
        <strong>Жанри:</strong>{" "}
        {show.genres?.map((g: any) => g.name).join(", ")}
      </p>
    
      <p><strong>Дата:</strong> {show.date}</p>
      <p><strong>Тривалість:</strong> {show.duration} хв</p>
      <p><strong>Ціна:</strong> {show.price} грн</p>
    </main>
  );
}
