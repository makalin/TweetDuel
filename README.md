# TweetDuel 🥊💬
### The Terminal-Based Debate AI That Turns Twitter Threads into Intellectual Battlegrounds

> *"Your tweet. Their takes. AI-powered counter-narratives. Let the duel begin."*

---

## 🔥 What is TweetDuel?

TweetDuel is a lightning-fast terminal tool that scrapes Twitter/X replies, analyzes arguments, and generates powerful counter-content using local LLMs. It's like having a debate champion AI that studies your tweet's replies and crafts devastating responses that spark viral discussions.

### Core Philosophy
- **Battle-Ready**: Every reply is a potential weapon
- **Viral by Design**: Generates content engineered for engagement
- **Privacy First**: Runs locally with Ollama, no data sent to Big Tech
- **Terminal Purity**: Fast, keyboard-driven, distraction-free

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **🎯 Smart Scraping** | Scrapes tweet replies without API keys using Snscrape |
| **🧠 AI Analysis** | Uses local LLMs (Ollama) to understand arguments and generate counters |
| **⚔️ Debate Engine** | Creates 3 types of responses: **Contrarian**, **Devil's Advocate**, **Nuance Master** |
| **📊 Thread Intelligence** | Maps conversation trees and identifies weak points |
| **🎭 Persona Modes** | 5 debate styles: *Socrates*, *Machiavelli*, *Chomsky*, *Tate*, *Neutral* |
| **💾 Content Arsenal** | Saves generated responses as drafts for later deployment |
| **🎪 Engagement Hacks** | Adds hooks, questions, and viral elements to responses |

---

## 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/makalin/TweetDuel.git
cd TweetDuel

# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not already)
curl https://ollama.ai/install.sh | sh

# Pull your preferred model
ollama pull llama3.2
# OR use mistral, deepseek, etc.
```

---

## ⚡ Quick Start

```bash
# Launch TweetDuel
python tweetduel.py

# Paste a tweet URL when prompted
🔗 Enter tweet URL: https://x.com/elonmusk/status/1234567890

# Watch the magic happen
🥊 Scraping replies...
🧠 Analyzing arguments...
⚔️ Generating counter-attacks...
```

---

## 🎮 Usage Modes

### 1. **Instant Duel Mode**
```bash
python tweetduel.py --url "TWEET_URL" --mode instant
```
Analyzes and generates responses immediately.

### 2. **Sniper Mode**
```bash
python tweetduel.py --url "TWEET_URL" --mode sniper
```
Waits for new replies and auto-generates counters.

### 3. **Armory Mode**
```bash
python tweetduel.py --url "TWEET_URL" --mode armory
```
Saves all generated content to deploy later strategically.

---

## 🎭 Debate Personas

| Persona | Style | Best For |
|---------|--------|----------|
| **Socrates** | Question-based, philosophical | Deep discussions |
| **Machiavelli** | Strategic, provocative | Controversial topics |
| **Chomsky** | Academic, evidence-based | Political debates |
| **Tate** | Aggressive, dominant | High-engagement threads |
| **Neutral** | Balanced, factual | Professional settings |

---

## 🧠 How it Works

### The TweetDuel Process:
1. **🎯 Target Acquisition**: Scrapes tweet and all replies
2. **🧬 DNA Analysis**: Breaks down arguments into logical components
3. **⚔️ Weakness Detection**: Identifies logical fallacies and gaps
4. **🎪 Counter-Creation**: Generates 3 response variants per reply
5. **📊 Viral Optimization**: Adds engagement hooks and questions
6. **💾 Arsenal Storage**: Saves everything for strategic deployment

---

## 🎪 Advanced Usage

### Custom AI Models
```bash
# Use different models for different styles
python tweetduel.py --model llama3.2 --persona socrates
python tweetduel.py --model mistral --persona tate
```

### Batch Processing
```bash
# Duel multiple tweets
python tweetduel.py --batch urls.txt --output duel_results.json
```

### Real-time Monitoring
```bash
# Watch a tweet for new replies
python tweetduel.py --watch --interval 300
```

---

## 🎨 Configuration

Create `~/.tweetduel/config.yaml`:

```yaml
ai:
  model: "llama3.2"
  temperature: 0.8
  max_tokens: 500

scraping:
  max_replies: 50
  include_quotes: true
  language_filter: "en"

debate:
  default_persona: "socrates"
  response_styles: ["contrarian", "devils_advocate", "nuanced"]
  viral_hooks: true
```

---

## 🚧 Roadmap

- [ ] **Image Reply Support**: Analyze and respond to image-based arguments
- [ ] **Multi-Language Battles**: Duel in Spanish, French, German
- [ ] **Thread Prediction**: AI predicts where discussions will go
- [ ] **Collaborative Duels**: Multiple AI personas team up
- [ ] **Analytics Dashboard**: Track which counters went viral
- [ ] **Twitter Bot Integration**: Auto-deploy responses (with approval)

---

## 🎯 Use Cases

- **🔥 Content Creators**: Generate viral counter-narratives
- **📊 Marketers**: Understand and counter competitor messaging
- **🎪 Trolls**: Professional-grade trolling (use responsibly!)
- **🧪 Researchers**: Study argument patterns and viral mechanics
- **📈 Growth Hackers**: Engineer engagement through controversy

---

## 🤝 Contributing

We welcome debate champions! See [CONTRIBUTING.md](CONTRIBUTING.md)

### Quick Start for Devs:
```bash
git clone https://github.com/makalin/TweetDuel.git
cd TweetDuel
pip install -r requirements-dev.txt
python -m pytest tests/
```

---

## ⚖️ Ethical Guidelines

TweetDuel is a powerful tool. Please:
- **🎯 Target ideas, not individuals**
- **🎪 Add value to discussions, don't just create chaos**
- **⚖️ Respect platform rules and rate limits**
- **🤝 Disclose AI use when appropriate**

---

## 📜 License

MIT License - Do whatever you want, but don't blame us if you start too many Twitter wars.

---

## 🏆 Hall of Fame

Best TweetDuel-generated responses:
- "Actually, the opposite is true..." - 50K likes
- "Let me play devil's advocate here..." - Started 500-reply thread
- "This ignores the fundamental..." - Changed OP's mind

---

## 🚨 Disclaimer

This tool is for educational and entertainment purposes. Users are responsible for how they deploy generated content. TweetDuel is not affiliated with Twitter/X.
