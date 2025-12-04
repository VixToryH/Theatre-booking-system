"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        setError("Невірний логін або пароль");
        return;
      }

      const data = await res.json();

      // зберігає токен
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      localStorage.setItem("username", username);
      
      const profileRes = await fetch("http://127.0.0.1:8000/api/users/me/", {
      headers: {
        "Authorization": `Bearer ${data.access}`,
      }
    });

    if (profileRes.ok) {
      const profile = await profileRes.json();
      localStorage.setItem("username", profile.username);
    }

      router.push("/");
      router.refresh();
    } catch {
      setError("Помилка сервера");
    }
  }

  return (
    <main className="relative min-h-screen flex items-center justify-center text-white">
      {/* фон */}
      <div
        className="absolute inset-0 bg-cover bg-center -z-10"
        style={{
          backgroundImage:
            "url('/961b7b0dc1b53ba44323412c167ee9f6.jpg')",
        }}
      />
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm -z-10" />

      {/* форма */}
      <div className="bg-black/40 p-10 rounded-2xl shadow-xl w-[380px] backdrop-blur-lg">
        <h1 className="text-3xl font-bold text-center mb-6">Увійти</h1>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="text"
            placeholder="Логін"
            className="w-full px-4 py-3 rounded-xl bg-transparent border border-white/40 text-white placeholder-white/40 focus:outline-none focus:border-white transition"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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

          {error && (
            <p className="text-red-400 text-center text-sm">{error}</p>
          )}

          <button
            className="w-full bg-white text-black font-semibold p-3 rounded-lg hover:bg-gray-200 transition"
          >
            Увійти
          </button>
        </form>

        <p className="text-center mt-4 text-sm opacity-80">
          Немає акаунта?{" "}
          <a href="/register" className="underline">
            Зареєструватися
          </a>
        </p>
      </div>
    </main>
  );
}
