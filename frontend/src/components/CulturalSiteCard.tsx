import { MapPin } from "lucide-react";
import { useState } from "react";

interface CulturalSiteCardProps {
  title: string;
  image: string;
  description: string;
  location: string;
  showFavoriteButton?: boolean;
}

export default function CulturalSiteCard({
  title,
  image,
  description,
  location,
  showFavoriteButton = true,
}: CulturalSiteCardProps) {
  const [isFavoriting, setIsFavoriting] = useState(false);

  const handleAddToFavorites = async () => {
    try {
      setIsFavoriting(true);
      const response = await fetch("http://127.0.0.1:8000/favorites", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ site_name: title }),
      });

      if (!response.ok) {
        throw new Error("Failed to add to favorites");
      }

      const result = await response.json();
      alert(result.message || "Added to favorites!");
    } catch (error) {
      console.error("Error adding to favorites:", error);
      alert("Failed to add to favorites");
    } finally {
      setIsFavoriting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-all duration-300 hover:shadow-2xl">
      <div className="relative h-64 overflow-hidden">
        <img src={image} alt={title} className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60"></div>
      </div>

      <div className="p-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-2">{title}</h3>

        <div className="flex items-center text-gray-600 mb-3">
          <MapPin size={16} className="mr-1 text-red-600" />
          <span className="text-sm">{location}</span>
        </div>

        <p className="text-gray-600 mb-4 line-clamp-3">{description}</p>

        {showFavoriteButton && (
          <div className="flex gap-2">
            <button
              onClick={handleAddToFavorites}
              disabled={isFavoriting}
              className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isFavoriting ? "Adding..." : "Favorite"}
            </button>
            <button className="flex-1 bg-gradient-to-r from-green-600 to-yellow-500 text-white py-2 px-4 rounded-lg font-semibold hover:from-green-700 hover:to-yellow-600 transition-all duration-200">
              Learn More
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
