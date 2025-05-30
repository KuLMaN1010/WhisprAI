import { useState, useRef } from "react";
import { getCoachingResponse } from "./api";
import brainIcon from './brain_icon.png';
import { MessageSquare } from "lucide-react";

export default function WhisprChat() {
  const [messages, setMessages] = useState([
    { sender: "agent", text: "How may we help you today?", timestamp: new Date() },
  ]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState("customer");
  const [coaching, setCoaching] = useState(null);
  const chatContainerRef = useRef(null);

  const handleSend = async () => {
    if (!input.trim()) return;
    const newMessage = { sender: mode, text: input.trim(), timestamp: new Date() };
    setMessages((msgs) => [...msgs, newMessage]);
    setInput("");

    if (mode === "customer") {
      const data = await getCoachingResponse(input.trim(), "");
      // expect { emotion, trigger, mindset, tone, cue }
      setCoaching({
        emotion: data.emotion,
        trigger: data.trigger,
        mindset: data.mindset,
        tone: data.tone,
        cue: data.cue
      });
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
    <div className="flex h-screen">
      {/* Left Sidebar */}
      <div className="w-1/3 bg-indigo-700 text-white p-6 flex flex-col">
        <div className="flex items-center mb-8">
          <img src={brainIcon} alt="WhisprAI" className="h-8 w-8 mr-2" />
          <div>
            <h1 className="text-2xl font-bold">WhisprAI</h1>
            <p className="text-sm opacity-75">Real-time agent assistance</p>
          </div>
        </div>
        <h2 className="font-semibold mb-4">WhisprAI Coaching</h2>
        <div className="flex-1 overflow-y-auto">
          {coaching ? (
            <div className="bg-indigo-100 text-indigo-900 p-4 rounded-lg">
              <p><strong>Emotion detected:</strong> {coaching.emotion}</p>
              <p><strong>Matching example trigger:</strong> {coaching.trigger}</p>
              <p><strong>Agent mindset to adopt:</strong> {coaching.mindset}</p>
              <p><strong>Suggested tone:</strong> {coaching.tone}</p>
              <p><strong>Coaching cue for next reply:</strong> {coaching.cue}</p>
            </div>
          ) : (
            <p className="text-indigo-200 text-sm">
              WhisprAI- Your AI Assistant who is here to help You ALWAYS!
              You name it. 
            </p>
          )}
        </div>
      </div>

      {/* Right Chat Panel */}
      <div className="w-2/3 flex flex-col bg-gray-100">
        {/* Header */}
        <div className="bg-white p-4 border-b shadow-sm flex items-center">
          <MessageSquare className="h-6 w-6 text-green-500 mr-3" />
          <div>
            <h2 className="font-semibold text-lg">Customer Service</h2>
            <p className="text-xs text-gray-500">Active conversation</p>
          </div>
        </div>

        {/* Messages */}
        <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.sender === 'agent' ? 'justify-end' : 'justify-start'}`}>
              <div className={`${msg.sender === 'agent' ? 'bg-blue-600 text-white' : 'bg-white text-gray-900'} p-3 rounded-lg max-w-xs shadow`}>
                <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                <div className="text-xs text-gray-500 text-right mt-1">
                  {formatTime(msg.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <div className="bg-white p-4 border-t">
          <label className="block text-xs text-gray-500 mb-1">
            {mode === 'customer' ? 'Customer:' : 'Agent:'}
          </label>
          <div className="flex">
            <input
              type="text"
              className="flex-1 border border-gray-300 px-4 py-2 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder={`Type your ${mode} message...`}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />
            <button onClick={handleSend} className="bg-indigo-600 text-white px-4 py-2 rounded-r-lg hover:bg-indigo-700">
              ➤
            </button>
          </div>
          <div className="mt-3 flex space-x-2">
            <button
              onClick={() => setMode('customer')}
              className={`px-3 py-1 rounded text-sm font-medium focus:outline-none transition-colors duration-200 ${
                mode === 'customer' ? 'bg-indigo-500 text-white' : 'bg-indigo-200 text-indigo-800 hover:bg-indigo-300'
              }`}
            >
              Customer Mode
            </button>
            <button
              onClick={() => setMode('agent')}
              className={`px-3 py-1 rounded text-sm font-medium focus:outline-none transition-colors duration-200 ${
                mode === 'agent' ? 'bg-indigo-500 text-white' : 'bg-indigo-200 text-indigo-800 hover:bg-indigo-300'
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
