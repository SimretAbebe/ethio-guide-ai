import CulturalSiteCard from "./CulturalSiteCard";
import { Sparkles } from "lucide-react";
import { getBaseUrl } from "../utils/api";

interface RecommendedSite {
  name: string;
  description: string;
  image: string;
  score: number;
  location?: string;
}

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState<RecommendedSite[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        const baseUrl = getBaseUrl();
        const response = await fetch(`${baseUrl}/recommendations`);
        if (!response.ok) {
          throw new Error("Failed to fetch recommendations");
        }
        const data = await response.json();
        setRecommendations(data);
      } catch (err) {
        console.error("Error fetching recommendations:", err);
        setError("Could not load recommendations at this time.");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  if (loading) {
    return (
      <div className="py-12 flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (error || recommendations.length === 0) {
    return null; 
  }

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center gap-2 mb-8">
          <Sparkles className="text-yellow-500" size={28} />
          <h2 className="text-3xl font-bold text-gray-800">Recommended for You</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {recommendations.map((site) => (
            <CulturalSiteCard
              key={site.name}
              title={site.name}
              description={site.description}
              image={site.image || "https://images.unsplash.com/photo-1523821741446-edb2b68bb7a0?q=80&w=2070"}
              location={site.location || "Ethiopia"}
              showFavoriteButton={true}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
