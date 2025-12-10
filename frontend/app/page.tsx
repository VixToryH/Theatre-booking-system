import RecommendedShows from "./components/RecommendedShows";

export default function HomePage() {
  return (
    <section className="relative w-full min-h-screen flex flex-col items-center justify-start pt-24">

      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center brightness-75"
        style={{
          backgroundImage: "url('/961b7b0dc1b53ba44323412c167ee9f6.jpg')",
          backgroundPosition: "center 68%",
        }}
      />

      {/* Плавне затемнення зверху */}
      <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-black/60 to-transparent z-0" />

      {/* Темний шар */}
      <div className="absolute inset-0 bg-black/25" />

      {/* Текст */}
      <div className="relative z-10 text-center max-w-3xl px-6 pt-48">
        <h1 className="text-5xl font-extrabold text-white drop-shadow-lg mb-6 leading-tight">
          Театр «Голос Емоцій»
        </h1>

        <p className="text-xl text-gray-200 mb-8 drop-shadow">
          Ласкаво просимо на сцену, де мистецтво говорить мовою почуттів.
        </p>

        <a
          href="/shows"
          className="inline-block bg-white text-black font-semibold py-3 px-8 rounded-full text-lg shadow-lg hover:bg-gray-200 transition"
        >
          Переглянути вистави
        </a>
      </div>

      {/* РЕКОМЕНДАЦІЇ */}
      <div className="relative z-10 w-full max-w-6xl mt-20 px-6">
        <RecommendedShows />
      </div>

    </section>
  );
}
