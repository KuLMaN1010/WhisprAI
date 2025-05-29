import { useState, useEffect, useRef } from "react";
import brainIcon from './brain_icon.png'; "react";
import { getCoachingResponse } from "./api";
import { ChatBubbleLeftIcon, ChatBubbleRightIcon, MoreHorizontalIcon } from "lucide-react";

export default function WhisprChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("customer");
  const [suggestions, setSuggestions] = useState([]);
  const chatContainerRef = useRef(null);

  const handleSend = async () => {
    if (!input.trim()) return;
    const newMessage = { sender: mode, text: input.trim(), timestamp: new Date() };
    setMessages((msgs) => [...msgs, newMessage]);
    setInput("");

    if (mode === "customer") {
      const data = await getCoachingResponse(input.trim(), "");
      setSuggestions(data.cue ? [data.cue] : []);
    }

    setTimeout(() => {
      if (chatContainerRef.current) {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
      }
    }, 100);
  };

  const formatTime = (date) =>
    date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className="flex h-screen font-sans">
      {/* Left Sidebar */}
      <div className="w-1/3 bg-indigo-700 text-white flex flex-col">
        <div className="p-6 flex items-center border-b border-indigo-600">
          <ChatBubbleLeftIcon className="w-8 h-8 mr-3" />
          <div>
            <h1 className="text-2xl font-bold">WhisprAI</h1>
            <p className="text-sm opacity-75">Real‑time agent assistance</p>
          </div>
        </div>
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-2">Suggested Responses</h2>
          <div className="text-indigo-200 text-sm">
            {suggestions.length === 0
              ? "WhisprAI coaching will appear here after each customer message."
              : null}
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {suggestions.map((sug, idx) => (
            <div
              key={idx}
              className="bg-indigo-100 text-indigo-900 p-3 rounded shadow-sm"
            >
              {sug}
            </div>
          ))}
        </div>
      </div>

      {/* Right Chat Panel */}
      <div className="w-2/3 flex flex-col bg-gray-50">
        {/* Header */}
        <div className="flex items-center justify-between bg-white p-4 border-b shadow-sm">
          <div className="flex items-center">
            <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center text-white font-bold mr-3">
              C
            </div>
            <div>
              <h2 className="font-semibold text-lg">Customer Support Chat</h2>
              <p className="text-xs text-gray-500">Active conversation</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <ChatBubbleRightIcon className="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer" />
            <MoreHorizontalIcon className="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer" />
          </div>
        </div>

        {/* Messages */}
        <div
          ref={chatContainerRef}
          className="flex-1 overflow-y-auto p-6 space-y-4"
        >
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.sender === 'agent' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`p-3 rounded-lg max-w-xs shadow ${
                  msg.sender === 'agent'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                <div className="text-xs text-gray-500 text-right mt-1">
                  {formatTime(msg.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="bg-white p-4 border-t">
          <label className="block text-xs text-gray-500 mb-1">
            {mode === 'customer' ? 'Customer:' : 'Agent:'}
          </label>

          <div className="flex items-center space-x-2">
            <input
              type="text"
              className="flex-1 border border-gray-300 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder={`Type your ${mode} message...`}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />
            <button
              onClick={handleSend}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              ➤
            </button>
          </div>

          <div className="mt-3 flex space-x-2">
            <button
              onClick={() => setMode('customer')}
              className={`px-3 py-1 rounded text-sm font-medium focus:outline-none ${
                mode === 'customer'
                  ? 'bg-gray-300'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              Customer Mode
            </button>
            <button
              onClick={() => setMode('agent')}
              className={`px-3 py-1 rounded text-sm font-medium focus:outline-none ${
                mode === 'agent'
                  ? 'bg-blue-200'
                  : 'bg-blue-100 hover:bg-blue-200'
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
