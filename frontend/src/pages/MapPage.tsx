import { useState, useEffect } from "react";
import EthiopiaMap from "../components/EthiopiaMap";
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
  images?: string[];
  coordinates?: {
    latitude: number;
    longitude: number;
  };
}

export default function MapPage() {
  const [sites, setSites] = useState<CulturalSite[]>([]);
  const [filteredSites, setFilteredSites] = useState<CulturalSite[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSite, setSelectedSite] = useState<CulturalSite | null>(null);

  useEffect(() => {
    const fetchSites = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch("http://127.0.0.1:8001/sites");

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data: CulturalSite[] = await response.json();
        setSites(data);
        setFilteredSites(data);
      } catch (err) {
        console.error("Error fetching cultural sites:", err);
        setError(
          err instanceof Error ? err.message : "Failed to fetch cultural sites"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchSites();
  }, []);

  const handleSearch = (search: string, category: string, region: string) => {
    let filtered = sites;

    if (search) {
      const searchLower = search.toLowerCase();
      filtered = filtered.filter(
        (site) =>
          site.name.toLowerCase().includes(searchLower) ||
          site.description.toLowerCase().includes(searchLower) ||
          site.location.toLowerCase().includes(searchLower)
      );
    }

    if (category) {
      filtered = filtered.filter((site) => site.category === category);
    }

    if (region) {
      filtered = filtered.filter((site) => site.region === region);
    }

    setFilteredSites(filtered);
    setSelectedSite(null); // Clear selection on filter change
  };

  const handleSiteSelect = (site: CulturalSite) => {
    setSelectedSite(site);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-20 w-20 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading map data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md mx-auto p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Could not load map
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
      <section className="bg-gradient-to-r from-green-600 to-yellow-500 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold mb-4">
            🗺️ Explore Ethiopia's Cultural Map
          </h1>
          <p className="text-lg max-w-2xl mx-auto">
            Discover historical sites, UNESCO heritage locations, and natural
            wonders across the beautiful landscape of Ethiopia
          </p>
        </div>
      </section>

      {/* Map Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Map */}
          <div className="lg:col-span-2">
            <EthiopiaMap 
              sites={filteredSites} 
              onSiteSelect={handleSiteSelect} 
              selectedSite={selectedSite}
            />
            <p className="text-sm text-gray-500 mt-2 text-center">
              Click on markers to view site details
            </p>
          </div>

          {/* Site Details Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6 sticky top-4">
              {selectedSite ? (
                <div>
                  <div className="flex items-center mb-4">
                    <span className="text-3xl mr-3"></span>
                    <h2 className="text-2xl font-bold text-gray-800">
                      {selectedSite.name}
                    </h2>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-start">
                      <span className="text-green-600 font-semibold w-24">
                        Location:
                      </span>
                      <span className="text-gray-700">
                        {selectedSite.location}
                      </span>
                    </div>

                    <div className="flex items-start">
                      <span className="text-green-600 font-semibold w-24">
                        Region:
                      </span>
                      <span className="text-gray-700">
                        {selectedSite.region}
                      </span>
                    </div>

                    <div className="flex items-start">
                      <span className="text-green-600 font-semibold w-24">
                        Category:
                      </span>
                      <span className="inline-block bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">
                        {selectedSite.category}
                      </span>
                    </div>

                    <div className="border-t pt-3 mt-3">
                      <p className="text-gray-600">{selectedSite.description}</p>
                    </div>

                    {selectedSite.historical_significance && (
                      <div className="border-t pt-3 mt-3">
                        <span className="text-green-600 font-semibold block mb-1">
                          Historical Significance:
                        </span>
                        <p className="text-gray-600 text-sm">
                          {selectedSite.historical_significance}
                        </p>
                      </div>
                    )}

                    {selectedSite.visiting_hours && (
                      <div className="flex items-start">
                        <span className="text-green-600 font-semibold w-24">
                          Hours:
                        </span>
                        <span className="text-gray-700">
                          {selectedSite.visiting_hours}
                        </span>
                      </div>
                    )}

                    {selectedSite.entry_fee !== undefined && (
                      <div className="flex items-start">
                        <span className="text-green-600 font-semibold w-24">
                          Entry Fee:
                        </span>
                        <span className="text-gray-700">
                          {selectedSite.entry_fee} ETB
                        </span>
                      </div>
                    )}

                    <div className="pt-6">
                      <a
                        href={`/site/${encodeURIComponent(selectedSite.name)}`}
                        className="block w-full text-center bg-green-600 text-white py-3 rounded-xl font-bold hover:bg-green-700 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5"
                      >
                         View Full Details & Photos
                      </a>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">
                    Select a Site
                  </h3>
                  <p className="text-gray-500">
                    Click on any marker on the map to view detailed information
                    about that cultural site
                  </p>
                </div>
              )}
            </div>

            {/* Sites List */}
            <div className="bg-white rounded-xl shadow-lg p-6 mt-6">
              <h3 className="text-lg font-bold text-gray-800 mb-4">
                All Sites ({filteredSites.length})
              </h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {filteredSites.map((site) => (
                  <button
                    key={site.name}
                    onClick={() => setSelectedSite(site)}
                    className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                      selectedSite?.name === site.name
                        ? "bg-green-100 text-green-800"
                        : "hover:bg-gray-100 text-gray-700"
                    }`}
                  >
                    <span className="font-medium">{site.name}</span>
                    <span className="text-sm text-gray-500 block">
                      {site.region}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

