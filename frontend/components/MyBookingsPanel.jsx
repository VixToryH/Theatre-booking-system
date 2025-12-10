"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { X } from "lucide-react";

export default function MyBookingsPanel({ open, onClose }) {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    if (!open) return;

    api
      .get("/api/bookings/my/")
      .then((res) => setBookings(res.data))
      .catch(() => setBookings([]));
  }, [open]);

  return (
    <div
      className={`fixed top-0 right-0 w-[380px] h-full bg-[#3b2411] text-white shadow-xl border-l border-black/20
      transform transition-transform duration-300 z-[9999]
      ${open ? "translate-x-0" : "translate-x-full"}`}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-white/20">
        <h2 className="text-2xl font-semibold">Мої бронювання</h2>
        <X className="cursor-pointer" size={28} onClick={onClose} />
      </div>

      {/* Content */}
      <div className="p-4 overflow-y-auto h-[calc(100%-70px)]">
        {bookings.length === 0 ? (
          <p className="text-white/70 text-center mt-10">
            У вас поки немає бронювань.
          </p>
        ) : (
          bookings.map((b) => (
            <div
              key={b.id}
              className="bg-white text-black rounded-xl p-4 mb-4 shadow border border-black/10"
            >
              <p><strong>Вистава:</strong> {b.show?.title}</p>
              <p><strong>Дата:</strong> {b.show?.date}</p>
              <p><strong>Час:</strong> {b.show?.time}</p>
              <p>
                <strong>Місце:</strong> ряд {b.seat?.row}, місце {b.seat?.number}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
