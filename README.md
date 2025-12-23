# ⚖️ DEBATE GRAVITY

> **AI-Powered Debate Arena** — Challenge an AI that argues the opposite of any position you take.

![Debate Gravity](https://img.shields.io/badge/AI-Gemini%202.0-00F0FF?style=for-the-badge)
![Flask](https://img.shields.io/badge/Backend-Flask-purple?style=for-the-badge)
![Tailwind](https://img.shields.io/badge/UI-Tailwind%20CSS-06B6D4?style=for-the-badge)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **AI Debate Opponent** | Powered by Google Gemini 2.0 Flash |
| 🎭 **3 Debate Modes** | Logical, Aggressive, Devil's Advocate |
| 💬 **Conversation Memory** | AI remembers context from previous exchanges |
| � **Debate Scoring** | Get scored on Logic, Evidence, Persuasion, Rebuttal |
| �🎤 **Voice Input** | Speak your arguments using Web Speech API |
| 🌙 **Theme Toggle** | Dark/Light mode with persistence |
| 🌟 **Particle Effects** | Floating neon particle background |
| ⌨️ **Typing Animation** | AI responses appear with typewriter effect |
| 🔊 **Sound Effects** | Audio feedback (toggleable) |
| 📱 **Mobile Friendly** | Responsive design with collapsible sidebar |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd Debate_Gravity
pip install -r requirements.txt
```

### 2. Configure API Key

Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Create a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Run

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser 🎉

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Ctrl + K` | Clear chat history |
| `Ctrl + M` | Toggle microphone |
| `Ctrl + /` | Toggle theme |

---

## 🗂️ Project Structure

```
Debate_Gravity/
├── app.py              # Flask backend + Gemini AI
├── requirements.txt    # Python dependencies
├── .env                # API key (create this)
├── .env.example        # API key template
└── templates/
    └── index.html      # Frontend UI
```

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-CORS
- **AI:** Google Gemini 2.0 Flash
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS
- **Features:** Web Speech API, LocalStorage, CSS Animations

---

## 📸 Screenshots

### Dark Mode
![Dark Mode](./screenshots/dark-mode.png)

### Light Mode
![Light Mode](./screenshots/light-mode.png)

*Note: Create a `screenshots` folder and add your images*

[![Watch the video](https://img.youtube.com/vi/2ZBClBr4e0I/0.jpg)](https://youtu.be/2ZBClBr4e0I)


---

## 🔧 Configuration

### Debate Modes

| Mode | Behavior |
|------|----------|
| **Logical** | Calm, academic counter-arguments |
| **Aggressive** | Sharp, forceful rebuttals |
| **Devil's Advocate** | Argues the opposite no matter what |

---

## 📝 API Reference

### POST `/chat`

Send a debate message to the AI with conversation history.

```json
{
  "message": "Climate change is real",
  "mode": "logical",
  "history": [
    {"user": "Previous message", "ai": "Previous response"}
  ]
}
```

**Response:**
```json
{
  "response": "While climate data shows warming trends...",
  "historyLength": 3
}
```

### POST `/score`

Score your debate performance (requires 2+ exchanges).

```json
{
  "history": [
    {"user": "...", "ai": "..."},
    {"user": "...", "ai": "..."}
  ]
}
```

**Response:**
```json
{
  "score": {
    "logic": 20,
    "evidence": 18,
    "persuasion": 22,
    "rebuttal": 15,
    "total": 75,
    "feedback": "Strong logical arguments. Add more evidence."
  }
}
```

### GET `/api/stats`

Get system status and debate statistics.

```json
{
  "status": "online",
  "count": 42,
  "recent": ["AI Safety", "Mars Colony"]
}
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

MIT License - feel free to use this for your hackathon! 🏆

---

## 👨‍💻 Author

Made with ❤️ for hackathons

---

> *"The measure of intelligence is the ability to change."* — Albert Einstein

