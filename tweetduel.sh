#!/bin/bash

# TweetDuel Launcher Script
# This script makes it easy to run TweetDuel with common options

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show help
show_help() {
    echo "TweetDuel Launcher Script 🥊💬"
    echo "================================"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -u, --url URL        Tweet URL to duel"
    echo "  -m, --mode MODE      Duel mode (instant, sniper, armory)"
    echo "  -p, --persona PERSONA Debate persona (socrates, machiavelli, chomsky, tate, neutral)"
    echo "  -c, --config FILE    Configuration file path"
    echo "  -h, --help           Show this help message"
    echo "  --demo               Run with demo data"
    echo ""
    echo "Examples:"
    echo "  $0 -u 'https://x.com/user/status/123' -p socrates"
    echo "  $0 --mode armory --url 'https://x.com/user/status/123'"
    echo "  $0 --demo"
    echo ""
}

# Function to check if Ollama is running
check_ollama() {
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_color $RED "❌ Ollama is not running!"
        echo ""
        echo "Please start Ollama first:"
        echo "  1. Install Ollama: curl https://ollama.ai/install.sh | sh"
        echo "  2. Start Ollama: ollama serve"
        echo "  3. Pull a model: ollama pull llama3.2"
        echo ""
        exit 1
    fi
    
    print_color $GREEN "✅ Ollama is running"
}

# Function to check Python dependencies
check_dependencies() {
    if ! python3 -c "import snscrape, rich, click, ollama" 2>/dev/null; then
        print_color $YELLOW "⚠️  Some dependencies are missing"
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
    fi
}

# Function to run demo
run_demo() {
    print_color $BLUE "🎮 Running TweetDuel Demo Mode"
    python3 examples/basic_duel.py
}

# Default values
URL=""
MODE="instant"
PERSONA="socrates"
CONFIG=""
DEMO=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--url)
            URL="$2"
            shift 2
            ;;
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -p|--persona)
            PERSONA="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG="$2"
            shift 2
            ;;
        --demo)
            DEMO=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_color $RED "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
main() {
    print_color $BLUE "🥊 TweetDuel Launcher 💬"
    echo ""
    
    # Check dependencies
    check_dependencies
    
    # Check Ollama (unless running demo)
    if [ "$DEMO" = false ]; then
        check_ollama
    fi
    
    echo ""
    
    # Run demo or main application
    if [ "$DEMO" = true ]; then
        run_demo
    else
        # Build command
        CMD="python3 tweetduel.py"
        
        if [ -n "$URL" ]; then
            CMD="$CMD --url '$URL'"
        fi
        
        if [ -n "$MODE" ]; then
            CMD="$CMD --mode $MODE"
        fi
        
        if [ -n "$PERSONA" ]; then
            CMD="$CMD --persona $PERSONA"
        fi
        
        if [ -n "$CONFIG" ]; then
            CMD="$CMD --config '$CONFIG'"
        fi
        
        print_color $GREEN "🚀 Launching TweetDuel..."
        echo "Command: $CMD"
        echo ""
        
        eval $CMD
    fi
}

# Run main function
main
