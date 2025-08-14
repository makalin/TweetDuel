#!/usr/bin/env python3
"""
Basic TweetDuel example - programmatic usage
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.scraper import TwitterScraper
from utils.ai_analyzer import AIAnalyzer
from utils.display import TweetDuelDisplay

def main():
    """Basic example of using TweetDuel programmatically"""
    
    # Initialize components
    display = TweetDuelDisplay()
    scraper = TwitterScraper(max_replies=5)  # Limit to 5 replies for demo
    analyzer = AIAnalyzer(model='llama3.2', temperature=0.8)
    
    # Show banner
    display.show_banner()
    
    # Example tweet URL (replace with real one)
    tweet_url = "https://x.com/elonmusk/status/1234567890"
    
    print(f"🔗 Analyzing tweet: {tweet_url}")
    
    # Extract tweet ID
    tweet_id = scraper.extract_tweet_id(tweet_url)
    if not tweet_id:
        print("❌ Invalid tweet URL")
        return
    
    print(f"📱 Tweet ID: {tweet_id}")
    
    # Note: In a real scenario, you would scrape actual data
    # For demo purposes, we'll use mock data
    print("⚠️  Note: This is a demo with mock data")
    print("   To use real data, ensure Ollama is running and use a real tweet URL")
    
    # Mock data for demonstration
    mock_tweet = {
        'id': tweet_id,
        'url': tweet_url,
        'content': "AI will revolutionize the world in the next decade. What do you think?",
        'author': 'elonmusk',
        'date': '2024-01-01T00:00:00',
        'likes': 15000,
        'retweets': 2500,
        'replies': 1200
    }
    
    mock_replies = [
        {
            'id': '1',
            'content': "AI is just hype. It won't change anything significant.",
            'author': 'skeptic_user',
            'date': '2024-01-01T00:05:00',
            'likes': 150,
            'retweets': 25,
            'replies': 10
        },
        {
            'id': '2',
            'content': "I agree! AI is already transforming industries. Look at ChatGPT!",
            'author': 'ai_enthusiast',
            'date': '2024-01-01T00:10:00',
            'likes': 300,
            'retweets': 50,
            'replies': 15
        }
    ]
    
    # Display the mock data
    display.show_duel_results(mock_tweet, mock_replies, [])
    
    # Show summary
    display.show_duel_summary(mock_tweet, mock_replies, [])
    
    print("\n🎯 This demonstrates the basic TweetDuel functionality.")
    print("   To run with real data:")
    print("   1. Start Ollama: ollama serve")
    print("   2. Pull a model: ollama pull llama3.2")
    print("   3. Run: python tweetduel.py --url 'YOUR_TWEET_URL'")

if __name__ == "__main__":
    main()
