import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import ImageGallery from "../components/ImageGallery";
import Reviews from "../components/Reviews";
import { getBaseUrl } from "../utils/api";

interface Review {
  user_name: string;
  rating: number;
  comment: string;
  created_at?: string;
}

interface Site {
  name: string;
  description: string;
  location: string;
  region: string;
  category: string;
  historical_significance?: string;
  visiting_hours?: string;
  entry_fee?: number;
  images: string[];
  reviews: Review[];
  average_rating: number;
}

export default function SiteDetailsPage() {
  const { name } = useParams<{ name: string }>();
  const [site, setSite] = useState<Site | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
      try {
        setLoading(true);
        const baseUrl = getBaseUrl();
        const response = await fetch(`${baseUrl}/sites/${name}`);
        if (!response.ok) throw new Error("Site not found");
        const data = await response.json();
        setSite(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load site");
      } finally {
        setLoading(false);
      }
    };

    fetchSite();
  }, [name]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-green-600"></div>
    </div>
  );

  if (error || !site) return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">Oops!</h2>
      <p className="text-gray-600 mb-8">{error || "Something went wrong"}</p>
      <Link to="/explore" className="bg-green-600 text-white px-8 py-3 rounded-full font-bold hover:bg-green-700 transition-all">
        Back to Explore
      </Link>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Hero Header */}
      <section className="bg-gradient-to-r from-green-700 to-green-500 text-white pt-24 pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div>
              <Link to="/explore" className="text-green-100 hover:text-white flex items-center mb-4 transition-colors">
                ← Back to Explorations
              </Link>
              <h1 className="text-4xl md:text-6xl font-black">{site.name}</h1>
              <div className="flex flex-wrap gap-4 mt-6">
                <span className="bg-white/20 backdrop-blur-md px-4 py-2 rounded-full text-sm font-semibold">{site.location}</span>
                <span className="bg-white/20 backdrop-blur-md px-4 py-2 rounded-full text-sm font-semibold">{site.region}</span>
                <span className="bg-yellow-400 text-yellow-900 px-4 py-2 rounded-full text-sm font-bold shadow-lg">{(site.average_rating || 0).toFixed(1)}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-20">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Gallery & Description */}
          <div className="lg:col-span-2 space-y-8">
            <div className="bg-white rounded-3xl p-6 shadow-xl border border-white">
              <ImageGallery images={site.images} />
            </div>

            <div className="bg-white rounded-3xl p-8 shadow-xl border border-white space-y-6">
              <h3 className="text-2xl font-bold text-gray-800 border-b pb-4">About this Site</h3>
              <p className="text-gray-600 leading-relaxed text-lg">{site.description}</p>
              
              {site.historical_significance && (
                <div className="bg-yellow-50 p-6 rounded-2xl border-l-8 border-yellow-400">
                  <h4 className="font-bold text-yellow-800 mb-2">Historical Significance</h4>
                  <p className="text-yellow-900">{site.historical_significance}</p>
                </div>
              )}
            </div>

            <div className="bg-white rounded-3xl p-8 shadow-xl border border-white">
              <Reviews 
                siteName={site.name} 
                reviews={site.reviews || []} 
                averageRating={site.average_rating || 0} 
                onReviewAdded={(newReview, newAverage) => {
                  setSite(prev => prev ? {
                    ...prev,
                    reviews: [newReview, ...prev.reviews],
                    average_rating: newAverage
                  } : null);
                }}
              />
            </div>
          </div>

          {/* Right Column: Key Details & Quick Info */}
          <div className="space-y-6">
            <div className="bg-white rounded-3xl p-8 shadow-xl border border-white sticky top-24">
              <h3 className="text-xl font-bold text-gray-800 mb-6">Quick Facts</h3>
              <div className="space-y-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center text-2xl"></div>
                  <div>
                    <span className="text-gray-400 text-sm block">Category</span>
                    <span className="font-bold text-gray-800">{site.category}</span>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-yellow-100 rounded-2xl flex items-center justify-center text-2xl"></div>
                  <div>
                    <span className="text-gray-400 text-sm block">Visiting Hours</span>
                    <span className="font-bold text-gray-800">{site.visiting_hours || "Contact for info"}</span>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center text-2xl"></div>
                  <div>
                    <span className="text-gray-400 text-sm block">Entry Fee</span>
                    <span className="font-bold text-gray-800">{site.entry_fee ? `${site.entry_fee} ETB` : "Free Entrance"}</span>
                  </div>
                </div>
              </div>

              <div className="mt-8 pt-8 border-t">
                 <button className="w-full bg-green-600 text-white py-4 rounded-2xl font-black text-lg shadow-green-200 shadow-2xl hover:bg-green-700 transition-all hover:-translate-y-1">
                    Book a Guide
                 </button>
                 <p className="text-xs text-center text-gray-400 mt-4">Safe & secure checkout provided by EthioPay</p>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
