"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== password2) {
      setError("Паролі не співпадають");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/api/users/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          email,
          password,
        }),
      });

      if (!res.ok) {
        const data = await res.json();

        const firstKey = Object.keys(data)[0];
        const firstError = Array.isArray(data[firstKey]) ? data[firstKey][0] : data[firstKey];

        setError(firstError || "Помилка реєстрації");
        return;
      }

      router.push("/login"); 
    } catch (err) {
      setError("Помилка сервера");
    }
  }
  

  return (
    <main className="relative min-h-screen flex items-center justify-center text-white">
      {/* фон */}
      <div
        className="absolute inset-0 bg-cover bg-center -z-10"
        style={{
          backgroundImage: "url('/961b7b0dc1b53ba44323412c167ee9f6.jpg')",
        }}
      />
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm -z-10" />

      {/* форма */}
      <div className="bg-black/40 p-10 rounded-2xl shadow-xl w-[380px] backdrop-blur-lg">
        <h1 className="text-3xl font-bold text-center mb-6">Реєстрація</h1>

        <form onSubmit={handleRegister} className="space-y-4">
          <input
            type="text"
            placeholder="Логін"
            className="w-full px-4 py-3 rounded-xl bg-transparent border border-white/40 text-white placeholder-white/40 focus:outline-none focus:border-white transition"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-3 rounded-xl bg-transparent border border-white/40 text-white placeholder-white/40 focus:outline-none focus:border-white transition"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Пароль"
            className="w-full px-4 py-3 rounded-xl bg-transparent border border-white/40 text-white placeholder-white/40 focus:outline-none focus:border-white transition"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Повторіть пароль"
            className="w-full px-4 py-3 rounded-xl bg-transparent border border-white/40 text-white placeholder-white/40 focus:outline-none focus:border-white transition"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            required
          />

          {error && (
            <p className="text-red-400 text-center text-sm">{error}</p>
          )}

          <button className="w-full bg-white text-black font-semibold p-3 rounded-lg hover:bg-gray-200 transition">
            Зареєструватися
          </button>
        </form>

        <p className="text-center mt-4 text-sm opacity-80">
          Вже є акаунт?{" "}
          <a href="/login" className="underline">
            Увійти
          </a>
        </p>
      </div>
    </main>
  );
}
