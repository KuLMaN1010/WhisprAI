import { useState, useRef } from "react";
import { getCoachingResponse } from "./api";

export default function WhisprChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("customer");
  // now holds an array of coaching-response objects
  const [suggestions, setSuggestions] = useState([]);
  const chatContainerRef = useRef(null);

  const handleSend = async () => {
    if (!input.trim()) return;

    // 1) add the new chat message
    const newMsg = { sender: mode, text: input.trim(), timestamp: new Date() };
    setMessages((m) => [...m, newMsg]);
    setInput("");

    // 2) if it's a customer message, call your real API
    if (mode === "customer") {
      try {
        const coach = await getCoachingResponse(input.trim(), "");
        // coach === { emotion, trigger, mindset, tone, cue }
        setSuggestions([coach]); 
      } catch (err) {
        console.error(err);
        setSuggestions([
          { cue: "Sorry, I couldn't reach the coaching server. Try again." },
        ]);
      }
    }

    // 3) scroll chat to bottom
    setTimeout(() => {
      chatContainerRef.current?.scrollTo(0, chatContainerRef.current.scrollHeight);
    }, 50);
  };

  const formatTime = (d) => d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Left Panel */}
      <div className="w-1/3 bg-indigo-700 text-white p-6 flex flex-col">
        <div className="flex items-center mb-8">
          <span className="text-3xl mr-2">💬</span>
          <div>
            <h1 className="text-2xl font-bold">WhisprAI</h1>
            <p className="text-sm opacity-75">Real-time agent assistance</p>
          </div>
        </div>

        <h2 className="font-semibold mb-4">WhisprAI Coaching</h2>
        <div className="flex-1 overflow-y-auto space-y-4">
          {suggestions.length === 0 ? (
            <p className="text-indigo-200 text-sm">
              Coaching cues will appear here after each customer message.
            </p>
          ) : (
            suggestions.map((s, i) => (
              <div key={i} className="bg-indigo-100 text-indigo-900 p-4 rounded-lg shadow">
                <p><strong>Emotion:</strong> {s.emotion}</p>
                <p><strong>Trigger:</strong> {s.trigger}</p>
                <p><strong>Mindset:</strong> {s.mindset}</p>
                <p><strong>Tone:</strong> {s.tone}</p>
                <p className="mt-2"><strong>Coaching Cue:</strong> {s.cue}</p>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-2/3 flex flex-col bg-gray-100">
        {/* header */}
        <div className="bg-white p-4 border-b shadow-sm flex items-center">
          <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-3">
            C
          </div>
          <div>
            <h2 className="font-semibold text-lg">Customer Support Chat</h2>
            <p className="text-xs text-gray-500">Active conversation</p>
          </div>
        </div>

        {/* messages */}
        <div
          ref={chatContainerRef}
          className="flex-1 overflow-y-auto p-6 space-y-4"
        >
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${
                m.sender === "agent" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`p-3 rounded-lg max-w-xs shadow ${
                  m.sender === "agent"
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-900"
                }`}
              >
                <p className="text-sm">{m.text}</p>
                <div className="text-xs text-gray-500 text-right mt-1">
                  {formatTime(m.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* input */}
        <div className="bg-white p-4 border-t">
          <label className="block text-xs text-gray-500 mb-1">
            {mode === "customer" ? "Customer:" : "Agent:"}
          </label>
          <div className="flex">
            <input
              type="text"
              className="flex-1 border border-gray-300 px-4 py-2 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder={`Type your ${mode} message…`}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button
              onClick={handleSend}
              className="bg-indigo-600 text-white px-4 py-2 rounded-r-lg hover:bg-indigo-700"
            >
              ➤
            </button>
          </div>
          <div className="mt-3 flex space-x-2">
            <button
              onClick={() => setMode("customer")}
              className={`px-3 py-1 rounded text-sm ${
                mode === "customer"
                  ? "bg-gray-300"
                  : "bg-gray-100 hover:bg-gray-200"
              }`}
            >
              Customer Mode
            </button>
            <button
              onClick={() => setMode("agent")}
              className={`px-3 py-1 rounded text-sm ${
                mode === "agent" ? "bg-blue-200" : "bg-blue-100 hover:bg-blue-200"
              }`}
            >
              Agent Mode
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
