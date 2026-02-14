import { useState } from "react";

interface Review {
  user_name: string;
  rating: number;
  comment: string;
  created_at?: string;
}

interface ReviewsProps {
  siteName: string;
  reviews: Review[];
  averageRating: number;
  onReviewAdded: (newReview: Review, newAverage: number) => void;
}

export default function Reviews({ siteName, reviews, averageRating, onReviewAdded }: ReviewsProps) {
  const [userName, setUserName] = useState("");
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userName || !comment) {
      setErrorMessage("Please fill in all fields");
      return;
    }

    try {
      setIsSubmitting(true);
      setErrorMessage("");
      const response = await fetch(`http://127.0.0.1:8001/sites/${siteName}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_name: userName, rating, comment }),
      });

      if (!response.ok) throw new Error("Failed to submit review");

      const data = await response.json();
      onReviewAdded(data.review, data.average_rating);
      
      // Reset form
      setUserName("");
      setRating(5);
      setComment("");
    } catch (err) {
      setErrorMessage("Error submitting review. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header & Stats */}
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold text-gray-800">Reviews & Ratings</h3>
        <div className="flex items-center bg-yellow-100 px-4 py-2 rounded-full">
          <span className="text-yellow-600 font-bold text-xl mr-2">★</span>
          <span className="text-yellow-800 font-bold">{averageRating.toFixed(1)}</span>
          <span className="text-gray-500 text-sm ml-2">({reviews.length} reviews)</span>
        </div>
      </div>

      {/* Review List */}
      <div className="space-y-4 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
        {reviews.length === 0 ? (
          <p className="text-gray-500 italic">No reviews yet. Be the first to share your experience!</p>
        ) : (
          reviews.map((review, idx) => (
            <div key={idx} className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-gray-800">{review.user_name}</span>
                <div className="flex text-yellow-500">
                  {[...Array(5)].map((_, i) => (
                    <span key={i}>{i < review.rating ? "★" : "☆"}</span>
                  ))}
                </div>
              </div>
              <p className="text-gray-600 text-sm">{review.comment}</p>
              {review.created_at && (
                <span className="text-xs text-gray-400 block mt-2">
                  {new Date(review.created_at).toLocaleDateString()}
                </span>
              )}
            </div>
          ))
        )}
      </div>

      {/* Submission Form */}
      <form onSubmit={handleSubmit} className="bg-green-50 rounded-2xl p-6 border-2 border-green-100">
        <h4 className="font-bold text-green-800 mb-4">Add your review</h4>
        {errorMessage && <p className="text-red-500 text-sm mb-4">{errorMessage}</p>}
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Your Name</label>
            <input
              type="text"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-green-500 outline-none"
              placeholder="e.g. Abebe"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Rating</label>
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => setRating(num)}
                  className={`w-10 h-10 rounded-full font-bold transition-all ${
                    rating === num ? "bg-green-600 text-white" : "bg-white text-gray-400 border border-gray-200 hover:bg-green-50"
                  }`}
                >
                  {num}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Your Comment</label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-green-500 outline-none h-24 resize-none"
              placeholder="Tell us about your visit..."
            ></textarea>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className={`w-full py-3 rounded-lg font-bold text-white transition-all ${
              isSubmitting ? "bg-gray-400 cursor-not-allowed" : "bg-green-600 hover:bg-green-700 shadow-lg hover:shadow-xl"
            }`}
          >
            {isSubmitting ? "Submitting..." : "Post Review"}
          </button>
        </div>
      </form>
    </div>
  );
}
