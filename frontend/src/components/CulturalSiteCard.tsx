import { MapPin } from "lucide-react";

interface CulturalSiteCardProps {
  title: string;
  image: string;
  description: string;
  location: string;
}

export default function CulturalSiteCard({
  title,
  image,
  description,
  location,
}: CulturalSiteCardProps) {
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

        <button className="w-full bg-gradient-to-r from-green-600 to-yellow-500 text-white py-2 px-4 rounded-lg font-semibold hover:from-green-700 hover:to-yellow-600 transition-all duration-200">
          Learn More
        </button>
      </div>
    </div>
  );
}
