import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { Icon } from "leaflet";
import "leaflet/dist/leaflet.css";

interface CulturalSite {
  name: string;
  description: string;
  location: string;
  region: string;
  category: string;
  coordinates?: {
    latitude: number;
    longitude: number;
  };
}

interface EthiopiaMapProps {
  sites: CulturalSite[];
  onSiteSelect?: (site: CulturalSite) => void;
}

// Custom marker icon
const customIcon = new Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

// Ethiopia center coordinates
const ETHIOPIA_CENTER: [number, number] = [9.145, 40.489];
const DEFAULT_ZOOM = 6;

export default function EthiopiaMap({ sites, onSiteSelect }: EthiopiaMapProps) {
  // Filter sites that have coordinates
  const sitesWithCoordinates = sites.filter(
    (site) => site.coordinates?.latitude && site.coordinates?.longitude
  );

  return (
    <div className="w-full h-[500px] rounded-xl overflow-hidden shadow-lg border-4 border-green-600">
      <MapContainer
        center={ETHIOPIA_CENTER}
        zoom={DEFAULT_ZOOM}
        className="w-full h-full"
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {sitesWithCoordinates.map((site) => (
          <Marker
            key={site.name}
            position={[site.coordinates!.latitude, site.coordinates!.longitude]}
            icon={customIcon}
            eventHandlers={{
              click: () => onSiteSelect?.(site),
            }}
          >
            <Popup>
              <div className="max-w-xs">
                <h3 className="font-bold text-lg text-green-700">{site.name}</h3>
                <p className="text-sm text-gray-600 mb-1">📍 {site.location}</p>
                <p className="text-sm text-gray-500 mb-2">{site.category}</p>
                <p className="text-sm line-clamp-3">{site.description}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
