import Hero from "../components/Hero";
import CulturalSiteCard from "../components/CulturalSiteCard";

export default function Home() {
  const culturalSites = [
    {
      title: "Rock-Hewn Churches of Lalibela",
      image:
        "https://as2.ftcdn.net/v2/jpg/04/16/05/59/1000_F_416055968_sBw34oi95UakEtB9UIbj1tOoiV4qr4Ja.jpg",
      description:
        "Eleven medieval monolithic churches carved out of rock in the 12th and 13th centuries. A UNESCO World Heritage site and one of Ethiopia's holiest cities.",
      location: "Lalibela, Amhara Region",
    },
    {
      title: "Simien Mountains",
      image:
        "https://as2.ftcdn.net/v2/jpg/01/07/88/63/1000_F_107886352_xGZ7Ru6wyeccVj8arEGwIMGXnoMHcHAQ.jpg",
      description:
        "Dramatic mountain peaks, deep valleys, and unique wildlife including the Gelada baboon. One of Africa's most spectacular mountain ranges.",
      location: "Amhara Region",
    },
    {
      title: "Axum",
      image:
        "https://as2.ftcdn.net/v2/jpg/05/54/73/31/1000_F_554733188_uHZ4HvipmNllQfZ5uMyRS7MDXRSVxDrQ.jpg",
      description:
        "Ancient capital of the Aksumite Empire, home to towering obelisks and the legendary resting place of the Ark of the Covenant.",
      location: "Tigray Region",
    },
    {
      title: "Fasil Ghebbi Castles",
      image:
        "https://as1.ftcdn.net/v2/jpg/02/04/12/64/1000_F_204126439_DuDTOYeoLxAQZPppUkUoTjEiGEiDqSst.jpg",
      description:
        "A fortress-city built by Emperor Fasilides in the 17th century, featuring magnificent castles and royal compounds in Gondar.",
      location: "Gondar, Amhara Region",
    },
    {
      title: "Walled City of Harar",
      image:
        "https://as1.ftcdn.net/v2/jpg/04/41/96/12/1000_F_441961297_uIFIYjhp0Nixq14EZgKAVRpBbSjzEIKL.jpg",
      description:
        "A sacred Islamic city with 82 mosques and over 100 shrines. Known for its unique cultural heritage and the famous hyena men.",
      location: "Harar, Harari Region",
    },
    {
      title: "Danakil Depression",
      image:
        "https://as2.ftcdn.net/v2/jpg/06/02/05/15/1000_F_602051533_nw1p3jZ9k9Q9fM65ut6ZYcL2U5o4Pgik.jpg",
      description:
        "One of the hottest and most alien-looking places on Earth, featuring colorful sulfur springs, salt flats, and active volcanoes.",
      location: "Afar Region",
    },
  ];

  return (
    <div>
      <Hero />

      <section
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16"
        id="explore"
      >
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">
            Discover <span className="text-green-600">Ethiopia's</span>{" "}
            Treasures
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            From ancient civilizations to natural wonders, explore the sites
            that make Ethiopia a unique destination
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {culturalSites.map((site) => (
            <CulturalSiteCard
              key={site.title}
              title={site.title}
              image={site.image}
              description={site.description}
              location={site.location}
            />
          ))}
        </div>
      </section>

      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-300">
            &copy; 2026 EthioGuide. Celebrating Ethiopia's Rich Heritage.
          </p>
        </div>
      </footer>
    </div>
  );
}
