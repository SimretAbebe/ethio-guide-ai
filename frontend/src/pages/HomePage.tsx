import { useState, useEffect } from "react";
import CulturalSiteCard from "../components/CulturalSiteCard";
import SearchBar from "../components/SearchBar";

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

export default function HomePage() {
  const [sites, setSites] = useState<CulturalSite[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSites = async (search = "", category = "", region = "") => {
    try {
      setLoading(true);
      setError(null);

      // Build query parameters
      const params = new URLSearchParams();
      if (search) params.append("search", search);
      if (category) params.append("category", category);
      if (region) params.append("region", region);

      const url = `http://127.0.0.1:8001/sites${params.toString() ? `?${params.toString()}` : ""}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: CulturalSite[] = await response.json();
      setSites(data);
    } catch (err) {
      console.error("Error fetching cultural sites:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch cultural sites");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSites();
  }, []);

  const handleSearch = (search: string, category: string, region: string) => {
    fetchSites(search, category, region);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading Ethiopian cultural sites...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Oops! Something went wrong</h2>
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
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-green-600 to-yellow-500 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Discover <span className="text-yellow-300">Ethiopia's</span> Rich Heritage
          </h1>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Explore ancient civilizations, UNESCO World Heritage sites, and natural wonders
            that make Ethiopia a unique destination in the world.
          </p>
        </div>
      </section>

      {/* Cultural Sites Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">
            Cultural Sites of <span className="text-green-600">Ethiopia</span>
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            From rock-hewn churches to ancient obelisks, discover the treasures that
            tell the story of Ethiopia's extraordinary heritage.
          </p>
        </div>

        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} />

        {sites.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-600 text-lg">No cultural sites found.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {sites.map((site, index) => (
              <CulturalSiteCard
                key={`${site.name}-${index}`}
                title={site.name}
                image={`https://source.unsplash.com/800x600/?${encodeURIComponent(site.name + ' ' + site.category)}`}
                description={site.description}
                location={site.location}
              />
            ))}
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

