"""
Twitter scraping utilities for TweetDuel
"""

import snscrape.modules.twitter as sntwitter
from typing import Dict, List, Optional
from datetime import datetime
import time

class TwitterScraper:
    """Twitter scraping utility class"""
    
    def __init__(self, max_replies: int = 50, include_quotes: bool = True):
        self.max_replies = max_replies
        self.include_quotes = include_quotes
    
    def extract_tweet_id(self, url: str) -> Optional[str]:
        """Extract tweet ID from Twitter URL"""
        try:
            if '/status/' in url:
                tweet_id = url.split('/status/')[1].split('?')[0]
                return tweet_id
            else:
                raise ValueError("Invalid Twitter URL format")
        except Exception as e:
            print(f"Error extracting tweet ID: {e}")
            return None
    
    def scrape_tweet(self, tweet_id: str) -> Optional[Dict]:
        """Scrape a single tweet"""
        try:
            for tweet in sntwitter.TwitterTweetScraper(tweet_id).get_items():
                return {
                    'id': tweet.id,
                    'url': tweet.url,
                    'content': tweet.rawContent,
                    'author': tweet.user.username,
                    'date': tweet.date.isoformat(),
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'replies': tweet.replyCount,
                    'quotes': getattr(tweet, 'quoteCount', 0)
                }
        except Exception as e:
            print(f"Error scraping tweet: {e}")
            return None
    
    def scrape_replies(self, tweet_id: str) -> List[Dict]:
        """Scrape replies to a tweet"""
        replies = []
        
        try:
            for reply in sntwitter.TwitterTweetScraper(tweet_id).get_items():
                if len(replies) >= self.max_replies:
                    break
                
                # Check if this is a reply to our target tweet
                if hasattr(reply, 'inReplyToTweetId') and reply.inReplyToTweetId == tweet_id:
                    reply_data = {
                        'id': reply.id,
                        'content': reply.rawContent,
                        'author': reply.user.username,
                        'date': reply.date.isoformat(),
                        'likes': reply.likeCount,
                        'retweets': reply.retweetCount,
                        'replies': reply.replyCount,
                        'quotes': getattr(reply, 'quoteCount', 0)
                    }
                    replies.append(reply_data)
                
                # Add small delay to be respectful
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error scraping replies: {e}")
        
        return replies
    
    def scrape_thread(self, tweet_id: str) -> Dict:
        """Scrape tweet and all replies"""
        tweet_data = self.scrape_tweet(tweet_id)
        if not tweet_data:
            return None
        
        replies = self.scrape_replies(tweet_id)
        
        return {
            'tweet': tweet_data,
            'replies': replies,
            'scraped_at': datetime.now().isoformat()
        }
    
    def get_user_tweets(self, username: str, limit: int = 10) -> List[Dict]:
        """Get recent tweets from a user"""
        tweets = []
        
        try:
            for tweet in sntwitter.TwitterUserScraper(username).get_items():
                if len(tweets) >= limit:
                    break
                
                tweet_data = {
                    'id': tweet.id,
                    'url': tweet.url,
                    'content': tweet.rawContent,
                    'date': tweet.date.isoformat(),
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'replies': tweet.replyCount,
                    'quotes': getattr(tweet, 'quoteCount', 0)
                }
                tweets.append(tweet_data)
                
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error scraping user tweets: {e}")
        
        return tweets
