import { useState, useEffect } from "react";
import CulturalSiteCard from "../components/CulturalSiteCard";

interface CulturalSite {
  name: string;
  description: string;
  location: string;
  region: string;
  category: string;
  historical_significance?: string;
  visiting_hours?: string;
  entry_fee?: number;
  coordinates?: {
    latitude: number;
    longitude: number;
  };
}

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState<CulturalSite[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFavorites = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch("http://127.0.0.1:8000/favorites");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: CulturalSite[] = await response.json();
      setFavorites(data);
    } catch (err) {
      console.error("Error fetching favorites:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch favorites");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, []);

  const handleRemoveFavorite = async (siteName: string) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/favorites/${encodeURIComponent(siteName)}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to remove from favorites");
      }

      // Refresh favorites list
      await fetchFavorites();
    } catch (err) {
      console.error("Error removing favorite:", err);
      alert("Failed to remove from favorites");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading your favorites...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Oops! Something went wrong
          </h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-green-600 to-yellow-500 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold mb-4">❤️ My Favorite Sites</h1>
          <p className="text-xl max-w-2xl mx-auto">
            Your personalized collection of Ethiopian cultural treasures
          </p>
        </div>
      </section>

      {/* Favorites Content */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {favorites.length === 0 ? (
          <div className="text-center py-16">
            <span className="text-8xl mb-6 block">📌</span>
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              No Favorites Yet
            </h2>
            <p className="text-gray-600 text-lg mb-8 max-w-md mx-auto">
              Start exploring Ethiopian cultural sites and add your favorites to
              create your personalized collection!
            </p>
            <a
              href="/explore"
              className="inline-block bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
            >
              Explore Sites
            </a>
          </div>
        ) : (
          <div>
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold text-gray-800">
                {favorites.length} {favorites.length === 1 ? "Site" : "Sites"}{" "}
                Saved
              </h2>
              <button
                onClick={() => fetchFavorites()}
                className="text-green-600 hover:text-green-700 font-medium"
              >
                🔄 Refresh
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {favorites.map((site) => (
                <div key={site.name} className="relative">
                  <CulturalSiteCard
                    title={site.name}
                    image={`https://source.unsplash.com/800x600/?${encodeURIComponent(site.name + " " + site.category)}`}
                    description={site.description}
                    location={site.location}
                    showFavoriteButton={false}
                  />
                  <button
                    onClick={() => handleRemoveFavorite(site.name)}
                    className="absolute top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-600 transition-colors shadow-lg z-10"
                    title="Remove from favorites"
                  >
                    🗑️ Remove
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-300">
            &copy; 2025 EthioGuide. Celebrating Ethiopia's Rich Heritage.
          </p>
        </div>
      </footer>
    </div>
  );
}
