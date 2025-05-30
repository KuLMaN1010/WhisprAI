Whispr.AI – Real‑Time Agent Coach



Live Demo: (if deployed)

🧠 Overview

Whispr.AI is a React‑powered customer support coaching tool that provides real‑time, AI‑driven guidance to support agents/reps. As a customer chats, Whispr.AI analyzes tone, emotion, 
and context—then surfaces concise coaching cues to help agents respond with empathy, clarity, and confidence.

This is a project built for hackathon and rapid prototyping, Whispr.AI demonstrates how retrieval‑augmented generation and custom prompting can elevate human interactions in customer service to improve/ advance the future of customer experience

✨ Features

Live Chat Interface: Two‑panel layout with customer messages on the right and coaching suggestions on the left.

Emotion & Tone Detection: Leverages a backend AI service to extract emotion, trigger, mindset, and tone from customer messages.

Dynamic Coaching Cues: Presents actionable advice and suggested phrasing to guide agent replies.

Dual Modes: Toggle between Customer and Agent modes to simulate both sides of the conversation flow (just for the sake of hackathon time constraints, can be updated later)

Responsive UI: Tailwind CSS layout inspired by leading chat apps for a familiar, clean experience.


🚀 Tech Stack

Frontend: React, Vite, Tailwind CSS, lucide‑react icons

Backend: Python Flask (or FastAPI) for RAG‑powered coaching API

AI: IBM watsonx.ai with custom prompt templates


📦 Installation Process

1. Clone the repo
   
2. Install dependencies
   npm install

3. Go to terminal

4.Start the backend (from /backend folder)
   pip install -r requirements.txt
   cd WhisprAI
   python backend_api.py

5. Run the frontend in another cmd (do not close them)
   cd frontend
   npm run dev

6. Open http://localhost:5173 in your browser.


   📝 Usage

Customer Mode: Enter a customer message to see it appear on the right panel.

Agent Mode: Use coaching cues from the left panel to craft your agent response.

Switch Modes: Click the 'Customer Mode' / 'Agent Mode' buttons to toggle input behavior.


Coaching Breakdown

On each customer message, Whispr.AI will display:

Emotion: The primary feeling detected from the customer.

Trigger: The key customer phrase that drove the emotion retrieved from the provided dataset and memory

Mindset: Recommended mindset that the agent should employ (e.g., empathetic, transparent).

Tone: Suggested tone attributes.

Coaching Cue: A cue generated with specific phrasing which the agent can reuse or adapt in their own reply.


🛠️ Configuration

API Endpoint: The frontend calls http://localhost:5000/coach—update src/api.js if you deploy elsewhere.

Tailwind: Styles live in src/index.css via CDN or PostCSS setup.

Icons: lucide‑react icon package powers chat bubble & mode toggles.


🤝 Contributing

Feel free to open issues or PRs for new features, bug fixes, or improvements.

1. Fork the repository

2. Create your feature branch (git checkout -b feature/YourFeature)

3. Commit your changes (git commit -m 'Add some feature')

4. Push to the branch (git push origin feature/YourFeature)

5. Open a Pull Request






Powered by retrieval‑augmented generation and human‑centric AI
