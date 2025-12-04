"use client";

import { useState } from "react";

export default function SeatsGrid({ showId, seats }: { showId: string; seats: any[] }) {
  const [selectedSeats, setSelectedSeats] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);

  const rowsMap: Record<number, any[]> = {};
  seats.forEach((seat) => {
    if (!rowsMap[seat.row]) rowsMap[seat.row] = [];
    rowsMap[seat.row].push(seat);
  });

  const cols = rowsMap[1]?.length || 0;

  function toggleSeat(seat: any) {
    if (!seat.is_available) return;

    setSelectedSeats((prev) =>
      prev.includes(seat.id)
        ? prev.filter((s) => s !== seat.id)
        : [...prev, seat.id]
    );
  }

  async function bookSeats() {
    if (selectedSeats.length === 0) return;

    setLoading(true);

    try {
      const token = localStorage.getItem("access");

      console.log("TOKEN FROM LOCALSTORAGE:", token);
      console.log("ALL LOCALSTORAGE:", JSON.stringify(localStorage, null, 2));

      const res = await fetch("http://127.0.0.1:8000/api/bookings/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
            },
        body: JSON.stringify({
          show: showId,
          seats: selectedSeats,
        }),
      });

      if (!res.ok) {
        alert("Помилка бронювання");
        return;
      }

      alert("Успішно заброньовано!");
      window.location.reload();
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="flex justify-center mt-10">
        <div className="bg-black/40 backdrop-blur-md p-8 rounded-2xl shadow-xl space-y-3">

          {Object.values(rowsMap).map((rowSeats, i) => (
            <div
              key={i}
              className="grid gap-3"
              style={{ gridTemplateColumns: `repeat(${cols}, 45px)` }}
            >
              {rowSeats.map((seat: any) => {
                const isSelected = selectedSeats.includes(seat.id);

                return (
                  <div key={seat.id} onClick={() => toggleSeat(seat)}>
                    <div
                      className={`
                        w-[45px] h-[45px] rounded-lg flex items-center justify-center 
                        cursor-pointer text-sm font-semibold transition-all duration-150
                        ${
                          !seat.is_available
                            ? "bg-gray-600 cursor-not-allowed"
                            : isSelected
                            ? "bg-blue-600 scale-105"
                            : seat.is_vip
                            ? "bg-yellow-500 hover:bg-yellow-400"
                            : "bg-green-600 hover:bg-green-500"
                        }
                      `}
                    >
                      {seat.row}.{seat.number}
                    </div>
                  </div>
                );
              })}
            </div>
          ))}

        </div>
      </div>

      <div className="flex justify-center mt-6 text-sm text-gray-200">
        <div className="flex gap-6">
          <Legend color="bg-green-600" text="Вільні" />
          <Legend color="bg-yellow-500" text="VIP" />
          <Legend color="bg-gray-600" text="Зайняті" />
          <Legend color="bg-blue-600" text="Обрані" />
        </div>
      </div>

      <div className="flex justify-center mt-8">
        <button
          onClick={bookSeats}
          disabled={loading}
          className="px-6 py-3 bg-blue-700 hover:bg-blue-600 rounded-xl text-white font-semibold disabled:bg-gray-500"
        >
          {loading ? "Бронювання..." : "Підтвердити бронювання"}
        </button>
      </div>
    </>
  );
}

function Legend({ color, text }: { color: string; text: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className={`w-4 h-4 rounded ${color}`}></span> {text}
    </div>
  );
}
