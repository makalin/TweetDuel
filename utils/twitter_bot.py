"""
Twitter bot integration for TweetDuel.
Posts replies via Twitter API v2 with user approval. Requires API keys in env or config.
"""

import os
from typing import Optional, Dict, Any, Tuple

try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False


def get_twitter_client(config: Optional[Dict[str, Any]] = None):
    """
    Build Tweepy client from env vars or config.
    Env: TWITTER_BEARER_TOKEN (or TWITTER_API_KEY + TWITTER_API_SECRET + TWITTER_ACCESS_TOKEN + TWITTER_ACCESS_SECRET)
    """
    if not TWEEPY_AVAILABLE:
        return None, "tweepy not installed. Run: pip install tweepy"

    config = config or {}
    twitter_config = config.get("twitter_bot", {})

    bearer = (
        os.environ.get("TWITTER_BEARER_TOKEN")
        or twitter_config.get("bearer_token")
    )
    if bearer:
        try:
            client = tweepy.Client(bearer_token=bearer)
            return client, None
        except Exception as e:
            return None, str(e)

    # OAuth 1.0a for posting (Bearer is read-only for most endpoints)
    api_key = os.environ.get("TWITTER_API_KEY") or twitter_config.get("api_key")
    api_secret = os.environ.get("TWITTER_API_SECRET") or twitter_config.get("api_secret")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN") or twitter_config.get("access_token")
    access_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET") or twitter_config.get("access_token_secret")

    if not all([api_key, api_secret, access_token, access_secret]):
        return None, "Twitter API credentials not set. Set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET (or bearer_token for read-only)."

    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
        api = tweepy.API(auth)
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )
        return client, None
    except Exception as e:
        return None, str(e)


def post_reply(
    client,
    tweet_id: str,
    text: str,
    config: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Post a reply to the given tweet_id. text must be <= 280 chars.
    Returns (success, error_message, response_data).
    """
    if not client:
        return False, "No Twitter client", None
    if len(text) > 280:
        text = text[:277] + "..."
    try:
        response = client.create_tweet(text=text, in_reply_to_tweet_id=str(tweet_id))
        data = getattr(response, "data", None) if response else None
        tid = None
        if data is not None:
            tid = data.get("id") if isinstance(data, dict) else getattr(data, "id", None)
        return True, None, {"id": tid}
    except Exception as e:
        return False, str(e), None


def is_bot_available(config: Optional[Dict[str, Any]] = None) -> bool:
    """Check if Twitter bot can be used (credentials + tweepy)."""
    client, err = get_twitter_client(config)
    return client is not None
