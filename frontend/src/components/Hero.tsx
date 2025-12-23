import { MapPin } from "lucide-react";

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-br from-green-600 via-yellow-500 to-red-600 text-white py-24 px-4">
      <div className="absolute inset-0 bg-black opacity-40"></div>

      <div className="relative max-w-7xl mx-auto text-center">
        <div className="flex justify-center mb-6">
          <MapPin size={64} className="text-white drop-shadow-lg" />
        </div>

        <h1 className="text-4xl md:text-6xl font-bold mb-6 drop-shadow-lg">
          Explore Ethiopia's Rich Cultural Heritage
        </h1>

        <p className="text-lg md:text-xl mb-8 max-w-2xl mx-auto drop-shadow-md">
          Discover ancient civilizations, breathtaking landscapes, and vibrant
          traditions in the cradle of humanity
        </p>

        <button className="bg-white text-green-700 px-8 py-3 rounded-full font-semibold text-lg hover:bg-gray-100 transform hover:scale-105 transition-all duration-200 shadow-xl">
          Start Exploring
        </button>
      </div>

      <div className="absolute bottom-0 left-0 right-0">
        <svg
          viewBox="0 0 1440 120"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z"
            fill="white"
          />
        </svg>
      </div>
    </div>
  );
}
