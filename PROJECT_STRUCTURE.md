# TweetDuel Project Structure 🏗️

## Overview
TweetDuel is a comprehensive AI-powered Twitter debate tool with a modular architecture designed for extensibility and maintainability.

## Directory Structure
```
TweetDuel/
├── 📁 .gitignore                 # Git ignore rules
├── 📁 README.md                  # Project documentation
├── 📁 requirements.txt           # Production dependencies
├── 📁 requirements-dev.txt       # Development dependencies
├── 📁 setup.py                   # Package setup and installation
├── 📁 Makefile                   # Development commands and automation
├── 📁 tweetduel.py              # Main application entry point
├── 📁 tweetduel.sh              # Shell launcher script
├── 📁 config.example.yaml        # Example configuration file
├── 📁 PROJECT_STRUCTURE.md       # This file
│
├── 📁 utils/                     # Utility modules
│   ├── 📁 __init__.py           # Package initialization
│   ├── 📁 config.py             # Configuration management
│   ├── 📁 scraper.py            # Twitter scraping utilities
│   ├── 📁 ai_analyzer.py        # AI analysis and generation
│   └── 📁 display.py            # Rich-based display utilities
│
├── 📁 tests/                     # Test suite
│   └── 📁 test_tweetduel.py     # Unit tests
│
├── 📁 examples/                  # Example scripts
│   └── 📁 basic_duel.py         # Basic usage example
│
├── 📁 duels/                     # Generated duel data (auto-created)
├── 📁 armory/                    # Saved responses (auto-created)
└── 📁 cache/                     # Cache files (auto-created)
```

## Core Components

### 🚀 Main Application (`tweetduel.py`)
- **Entry Point**: CLI interface using Click
- **Core Logic**: TweetDuel class with all main functionality
- **Modes**: Instant, Sniper, and Armory modes
- **Personas**: 5 debate styles (Socrates, Machiavelli, Chomsky, Tate, Neutral)

### ⚙️ Configuration (`utils/config.py`)
- **Default Config**: Sensible defaults for all settings
- **File Management**: Automatic config file creation and loading
- **Validation**: Configuration validation and error handling

### 🕷️ Scraping (`utils/scraper.py`)
- **Twitter Integration**: Uses snscrape for data extraction
- **Rate Limiting**: Respectful scraping with delays
- **Data Processing**: Clean, structured data extraction

### 🤖 AI Analysis (`utils/ai_analyzer.py`)
- **Ollama Integration**: Local LLM support
- **Argument Analysis**: Logical fallacy detection
- **Response Generation**: Persona-based counter-arguments
- **Viral Optimization**: Engagement-focused content

### 🎨 Display (`utils/display.py`)
- **Rich Integration**: Beautiful terminal output
- **Tables & Panels**: Structured information display
- **Interactive Prompts**: User-friendly interface

## Key Features

### 🎯 Core Functionality
- **Smart Scraping**: Extract tweets and replies without API keys
- **AI Analysis**: Understand arguments and identify weaknesses
- **Persona System**: 5 distinct debate styles
- **Response Generation**: Create viral counter-arguments
- **Content Management**: Save and organize responses

### 🎮 Operation Modes
1. **Instant Mode**: Quick analysis and response generation
2. **Sniper Mode**: Monitor for new replies (concept)
3. **Armory Mode**: Strategic response deployment

### 🎭 Debate Personas
- **Socrates**: Question-based, philosophical
- **Machiavelli**: Strategic, provocative
- **Chomsky**: Academic, evidence-based
- **Tate**: Aggressive, dominant
- **Neutral**: Balanced, factual

## Development Workflow

### 🛠️ Setup Commands
```bash
# Install dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean up
make clean
```

### 🚀 Running the Application
```bash
# Direct Python execution
python tweetduel.py --url "TWEET_URL" --persona socrates

# Using shell script
./tweetduel.sh -u "TWEET_URL" -p socrates

# Demo mode
./tweetduel.sh --demo
```

### 📦 Package Management
```bash
# Install locally for development
make install-local

# Build package
make build

# Check setup
make check-setup
```

## Dependencies

### 🔧 Production Dependencies
- **snscrape**: Twitter data extraction
- **ollama**: Local LLM integration
- **rich**: Beautiful terminal output
- **click**: CLI framework
- **pyyaml**: Configuration management

### 🧪 Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

## Configuration

### ⚙️ Default Settings
- **AI Model**: llama3.2
- **Temperature**: 0.8 (creative)
- **Max Replies**: 50
- **Default Persona**: Socrates
- **Ollama Host**: localhost:11434

### 📁 Configuration Files
- **User Config**: `~/.tweetduel/config.yaml`
- **Example Config**: `config.example.yaml`
- **Runtime Config**: Command line options

## Testing

### 🧪 Test Coverage
- **Unit Tests**: Core functionality testing
- **Mock Testing**: External service mocking
- **Configuration Tests**: Settings validation
- **Integration Tests**: Component interaction

### 📊 Test Commands
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
python -m pytest tests/test_tweetduel.py -v
```

## Deployment

### 🚀 Installation Options
1. **Development**: `make install-local`
2. **System-wide**: `pip install .`
3. **User-specific**: `pip install --user .`

### 📋 Prerequisites
- Python 3.8+
- Ollama running locally
- LLM model downloaded (e.g., `ollama pull llama3.2`)

## Extensibility

### 🔌 Plugin Architecture
- **Modular Design**: Easy to add new features
- **Utility Classes**: Reusable components
- **Configuration**: Flexible settings system
- **Persona System**: Easy to add new debate styles

### 🎯 Future Enhancements
- **Image Analysis**: Respond to image-based arguments
- **Multi-language**: Support for different languages
- **API Integration**: Direct Twitter API support
- **Collaborative Duels**: Multiple AI personas team up

## Contributing

### 🤝 Development Guidelines
- **Code Style**: Follow Black formatting
- **Testing**: Add tests for new features
- **Documentation**: Update relevant docs
- **Type Hints**: Use Python type annotations

### 📝 Pull Request Process
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Code review and merge

---

*This structure provides a solid foundation for the TweetDuel project, with clear separation of concerns and easy extensibility.*
