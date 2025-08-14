"""
Tests for TweetDuel
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import get_default_config, load_config
from utils.scraper import TwitterScraper
from utils.ai_analyzer import AIAnalyzer

class TestConfig(unittest.TestCase):
    """Test configuration utilities"""
    
    def test_get_default_config(self):
        """Test default configuration structure"""
        config = get_default_config()
        
        self.assertIn('ai', config)
        self.assertIn('scraping', config)
        self.assertIn('debate', config)
        self.assertIn('ollama_host', config)
        
        self.assertEqual(config['ai']['model'], 'llama3.2')
        self.assertEqual(config['ai']['temperature'], 0.8)
        self.assertEqual(config['scraping']['max_replies'], 50)

class TestTwitterScraper(unittest.TestCase):
    """Test Twitter scraping utilities"""
    
    def setUp(self):
        self.scraper = TwitterScraper()
    
    def test_extract_tweet_id_valid(self):
        """Test valid tweet ID extraction"""
        url = "https://x.com/username/status/1234567890"
        tweet_id = self.scraper.extract_tweet_id(url)
        self.assertEqual(tweet_id, "1234567890")
    
    def test_extract_tweet_id_invalid(self):
        """Test invalid tweet ID extraction"""
        url = "https://x.com/username"
        tweet_id = self.scraper.extract_tweet_id(url)
        self.assertIsNone(tweet_id)
    
    def test_extract_tweet_id_with_params(self):
        """Test tweet ID extraction with URL parameters"""
        url = "https://x.com/username/status/1234567890?ref_src=twsrc%5Etfw"
        tweet_id = self.scraper.extract_tweet_id(url)
        self.assertEqual(tweet_id, "1234567890")

class TestAIAnalyzer(unittest.TestCase):
    """Test AI analysis utilities"""
    
    def setUp(self):
        self.analyzer = AIAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test AI analyzer initialization"""
        self.assertEqual(self.analyzer.model, 'llama3.2')
        self.assertEqual(self.analyzer.temperature, 0.8)
        self.assertEqual(self.analyzer.max_tokens, 500)
    
    @patch('ollama.Client')
    def test_analyze_arguments(self, mock_client):
        """Test argument analysis (mocked)"""
        mock_response = Mock()
        mock_response.__getitem__.return_value = '{"main_arguments": ["test"]}'
        mock_client.return_value.generate.return_value = mock_response
        
        analyzer = AIAnalyzer()
        result = analyzer.analyze_arguments("Test content")
        
        self.assertIn('main_arguments', result)

if __name__ == '__main__':
    unittest.main()
