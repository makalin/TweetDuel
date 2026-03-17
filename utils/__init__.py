"""
TweetDuel utilities package
"""

from .config import load_config, get_default_config, save_config, create_default_config
from .scraper import TwitterScraper
from .ai_analyzer import AIAnalyzer
from .display import TweetDuelDisplay
from .i18n import t, set_default_language, get_supported_languages
from .reports import generate_report, generate_html_report, generate_text_report
from .tools import export_duel_markdown, export_duel_json, get_duel_stats, load_duel, list_duel_files, list_armory_files
from .twitter_bot import get_twitter_client, post_reply, is_bot_available

__all__ = [
    'load_config',
    'get_default_config',
    'save_config',
    'create_default_config',
    'TwitterScraper',
    'AIAnalyzer',
    'TweetDuelDisplay',
    't',
    'set_default_language',
    'get_supported_languages',
    'generate_report',
    'generate_html_report',
    'generate_text_report',
    'export_duel_markdown',
    'export_duel_json',
    'get_duel_stats',
    'load_duel',
    'list_duel_files',
    'list_armory_files',
    'get_twitter_client',
    'post_reply',
    'is_bot_available',
]
