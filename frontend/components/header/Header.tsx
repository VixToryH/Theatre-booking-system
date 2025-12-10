"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import MyBookingsPanel from "@/components/MyBookingsPanel";

export default function Header() {
  const router = useRouter();
  const [username, setUsername] = useState<string | null>(null);
  const [showPanel, setShowPanel] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access");
    const user = localStorage.getItem("username");

    if (token && user) {
      setUsername(user);
    }
  }, []);

  function handleLogout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("username");

    setUsername(null);
    router.push("/login");
  }

  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-transparent">
      <div className="w-full max-w-[1600px] mx-auto flex items-center justify-between py-4 px-8 text-white">

        {/* Лого */}
        <div className="flex-1">
          <Link 
            href="/" 
            className="text-2xl font-bold tracking-tight hover:opacity-80 transition"
          >
            Театр «Голос Емоцій»
          </Link>
        </div>

        {/* Правий блок */}
        <div className="flex items-center gap-4">

          {!username ? (
            <>
              <Link href="/register">
                <Button className="px-5 py-2 text-base rounded-xl shadow-lg bg-white/10 text-white border border-white/50 hover:bg-white/20 transition">
                  Зареєструватись
                </Button>
              </Link>

              <Link href="/login">
                <Button className="px-5 py-2 text-base rounded-xl shadow-lg bg-white text-black hover:bg-gray-200 transition">
                  Увійти
                </Button>
              </Link>
            </>
          ) : (
            <div className="flex items-center gap-3">

              {/* Кнопка МОЇ БРОНЮВАННЯ */}
              <Button
                onClick={() => setShowPanel(true)}
                className="bg-[#4B2E15] hover:bg-[#3b2411] px-4 py-2 rounded-xl text-white shadow-lg mt-1"
              >
                Мої бронювання
              </Button>

              <span className="text-white font-medium text-lg">
                {username}
              </span>

              <Button 
                className="bg-red-600 hover:bg-red-700 text-white px-5 py-2 rounded-xl"
                onClick={handleLogout}
              >
                Вийти
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Панель бронювань */}
      <MyBookingsPanel open={showPanel} onClose={() => setShowPanel(false)} />
    </header>
  );
}
