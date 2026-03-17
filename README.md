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
| **📄 Reports** | Generate HTML, text, or JSON reports of duels |
| **🔮 Thread Prediction** | AI predicts where the discussion will go |
| **🤖 Twitter Bot** | Post counter-replies to Twitter (with approval) via API |
| **🌍 Multi-Language** | UI and output in English, Turkish, Spanish, German, French |
| **📊 Tools** | Batch URLs, stats, export to Markdown/JSON |

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

## 📦 Build & run from any folder

Install TweetDuel once so you can run it from **any directory** on your PC:

```bash
# From the TweetDuel project folder
cd TweetDuel

# Option A: Editable install (recommended for development)
# Changes to code take effect immediately; run from anywhere
pip install -e .

# Option B: Normal install (for using as a fixed app)
pip install .
```

Then run from **any folder**:

```bash
# Run from anywhere (no need to cd to TweetDuel)
tweetduel
tweetduel --url "https://x.com/user/status/123" --lang tr
tweetduel --stats
```

**Windows (PowerShell or CMD):** Same as above after `pip install -e .` — the `tweetduel` command is on your PATH.

**Using Python module (no install):** From any folder, if the project is on `PYTHONPATH` or you run from project root:

```bash
cd C:\inetpub\wwwroot\TweetDuel
python -m tweetduel
```

**Run scripts (no install):** From the project folder you can use:
- **Windows CMD:** `run.bat` or `run.bat --url "https://..."`
- **PowerShell:** `.\run.ps1` or `.\run.ps1 --stats`
- Set `TWEETDUEL_HOME` to the TweetDuel folder to use `run.bat` from elsewhere; data dirs (duels, armory, etc.) will be created in the project folder.

**Note:** When you run the installed `tweetduel` command, duels, armory, cache, and reports are created in the **current working directory**. Config is stored in `~/.tweetduel/config.yaml` (or `%USERPROFILE%\.tweetduel\config.yaml` on Windows).

---

## ⚡ Quick Start

```bash
# From project folder (without install)
python tweetduel.py

# Or after "pip install -e ." — from any folder
tweetduel

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
# Duel multiple tweets (one URL per line in urls.txt)
python tweetduel.py --batch urls.txt
```

### Reports
```bash
# Generate HTML report after duel
python tweetduel.py -u "TWEET_URL" --report html --report-out reports/my_duel.html

# Text or JSON report
python tweetduel.py -u "TWEET_URL" --report text
```

### Thread Prediction
```bash
# Only run thread prediction (no counters)
python tweetduel.py -u "TWEET_URL" --predict-only
```

### Twitter Bot (post with approval)
**Use environment variables only—never put API keys in config files committed to git.** (See *Security* below.)
```bash
# Set env: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
# Then run with --post to be prompted to post each counter-reply
python tweetduel.py -u "TWEET_URL" --post
```

### Multi-Language (including Turkish)
```bash
# Turkish UI and output
python tweetduel.py -u "TWEET_URL" --lang tr

# Or set in config: language: "tr"
```

### Stats & Export
```bash
# Show duel and armory stats
python tweetduel.py --stats

# Export last duel to Markdown or JSON
python tweetduel.py --export md
python tweetduel.py --export json
```

---

## 🎨 Configuration

Create `~/.tweetduel/config.yaml` (or copy from `config.example.yaml`). **Do not put API keys or secrets in any file you commit to git—use environment variables.** (See *Security* below.)

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

# UI language: en, tr, es, de, fr
language: "en"

# Optional Twitter API (or use env vars)
twitter_bot:
  enabled: false

reports:
  default_format: "html"
  output_dir: "reports"
```

---

## 🚧 Roadmap

- [x] **Multi-Language**: English, Turkish, Spanish, German, French
- [x] **Thread Prediction**: AI predicts where discussions will go
- [x] **Twitter Bot Integration**: Post responses with approval (env: `TWITTER_*`)
- [x] **Reports**: HTML, text, JSON reports
- [ ] **Image Reply Support**: Analyze and respond to image-based arguments
- [ ] **Collaborative Duels**: Multiple AI personas team up
- [ ] **Analytics Dashboard**: Track which counters went viral

---

## 🎯 Use Cases

- **🔥 Content Creators**: Generate viral counter-narratives
- **📊 Marketers**: Understand and counter competitor messaging
- **🎪 Trolls**: Professional-grade trolling (use responsibly!)
- **🧪 Researchers**: Study argument patterns and viral mechanics
- **📈 Growth Hackers**: Engineer engagement through controversy

---

## 🔒 Security

**Do not commit API keys or secrets.** Use **environment variables** for Twitter: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET` (or `TWITTER_BEARER_TOKEN`). Don’t put them in `config.yaml` or any committed file. User config in `~/.tweetduel/config.yaml` is outside the repo. Git ignores: `config.yaml`, `.env`, `.env.*`, `secrets.yaml`, `*secrets*`, `credentials*`, and data dirs (`duels/`, `armory/`, `reports/`). If you leak a key, rotate it immediately in the Twitter Developer Portal; it remains in git history otherwise. The app redacts secrets when showing config.

---

## 📁 Project structure

```
TweetDuel/
├── tweetduel.py          # Main entry, CLI (Click)
├── config.example.yaml   # Example config (copy to ~/.tweetduel/config.yaml)
├── setup.py, requirements.txt
├── utils/
│   ├── config.py         # Config load/save
│   ├── scraper.py        # Twitter scraping (snscrape)
│   ├── ai_analyzer.py    # Ollama analysis, counters, thread prediction
│   ├── display.py        # Rich terminal UI
│   ├── i18n.py           # Multi-language (en, tr, es, de, fr)
│   ├── reports.py        # HTML/text/JSON reports
│   ├── tools.py          # Export, batch, stats
│   └── twitter_bot.py    # Twitter API posting (env vars only)
├── tests/
├── examples/
├── duels/                 # Generated duel data (auto-created, gitignored)
├── armory/                # Saved responses (auto-created, gitignored)
└── reports/               # Report output (auto-created, gitignored)
```

**Dev commands:** `make install-dev`, `make test`, `make format`, `make lint`, `make install-local`, `make build`.

---

## 🤝 Contributing

PRs welcome. Dev setup: `pip install -r requirements-dev.txt`, then `python -m pytest tests/`. Use Black for formatting.

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
