import { useState } from "react";
import { getCoachingResponse } from './api';

export default function WhisprAI() {
  const [customer, setCustomer] = useState("");
  const [agent, setAgent] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!customer.trim() || !agent.trim()) return;

    setLoading(true);
    setResponse(null);

    const res = await fetch("http://localhost:5000/api/coach", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ customer, agent }),
  });
    const data = await res.json();
    setResponse(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-6">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
          🧠 Whispr.AI Coaching
        </h1>

        <label className="block mb-2 text-sm font-medium text-gray-700">
          Customer Message
        </label>
        <textarea
          rows="3"
          className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
          value={customer}
          onChange={(e) => setCustomer(e.target.value)}
        ></textarea>

        <label className="block mt-4 mb-2 text-sm font-medium text-gray-700">
          Agent Reply
        </label>
        <textarea
          rows="2"
          className="w-full p-3 border rounded-xl focus:outline-none focus:ring"
          value={agent}
          onChange={(e) => setAgent(e.target.value)}
        ></textarea>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="mt-6 w-full bg-indigo-600 text-white font-semibold py-3 rounded-xl hover:bg-indigo-700 transition"
        >
          {loading ? "Coaching..." : "Get Coaching Cue"}
        </button>

        {response && (
          <div className="mt-8 bg-gray-50 border rounded-xl p-4">
            {response.error ? (
              <p className="text-red-500">{response.error}</p>
            ) : (
              <>
                <p><strong>Emotion detected:</strong> {response.emotion}</p>
                <p><strong>Matching trigger:</strong> {response.trigger}</p>
                <p><strong>Agent mindset:</strong> {response.mindset}</p>
                <p><strong>Suggested tone:</strong> {response.tone}</p>
                <p><strong>Coaching cue:</strong> {response.cue}</p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
