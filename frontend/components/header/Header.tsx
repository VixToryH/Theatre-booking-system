"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function Header() {
  const pathname = usePathname();

  const menu = [
    { label: "Про театр", href: "/about" },
  ];

  const isLoggedIn = false;

  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-transparent">
      <div className="w-full max-w-[1600px] mx-auto flex items-center justify-between py-4 px-8 text-white">
        
        {/* ЛОГО ЗЛІВА (прибито до краю) */}
        <div className="flex-1">
          <Link 
            href="/" 
            className="text-2xl font-bold tracking-tight flex items-center gap-2 hover:opacity-80 transition"
          >
            Театр «Голос Емоцій»
          </Link>
        </div>

        {/* МЕНЮ СТРОГО ПО ЦЕНТРУ */}
        <nav className="absolute left-1/2 -translate-x-1/2 hidden md:flex">
          {menu.map((item) => {
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.label}
                href={item.href}
                className={`mx-6 text-lg font-semibold transition 
                  ${isActive 
                    ? "text-white border-b-2 border-white pb-1" 
                    : "text-gray-300 hover:text-white"
                  }`
                }
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* КНОПКИ СПРАВА */}
        <div className="flex-1 flex justify-end gap-4">
          {!isLoggedIn ? (
            <>
              <Link href="/register">
                <Button 
                  className="px-5 py-2 text-base rounded-xl shadow-lg bg-white/10 text-white border border-white/50 hover:bg-white/20 transition"
                >
                  Зареєструватись
                </Button>
              </Link>

              <Link href="/login">
                <Button 
                  className="px-5 py-2 text-base rounded-xl shadow-lg bg-white text-black hover:bg-gray-200 transition"
                >
                  Увійти
                </Button>
              </Link>
            </>
          ) : (
            <>
              <Link href="/profile">
                <Button variant="secondary">Профіль</Button>
              </Link>
              <Button variant="destructive">Вийти</Button>
            </>
          )}
        </div>

      </div>
    </header>
  );
}
