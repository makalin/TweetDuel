#!/usr/bin/env python3
"""
TweetDuel 🥊💬
The Terminal-Based Debate AI That Turns Twitter Threads into Intellectual Battlegrounds
"""

import os
import sys
import json
import asyncio
import argparse
import yaml
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse

import click
import rich
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich.markdown import Markdown

import snscrape.modules.twitter as sntwitter
import requests
from bs4 import BeautifulSoup
import ollama

from utils.i18n import t, set_default_language, get_supported_languages
from utils.reports import generate_report
from utils.tools import export_duel_markdown, export_duel_json, get_duel_stats, list_armory_files, load_duel
from utils.twitter_bot import get_twitter_client, post_reply, is_bot_available

# Initialize Rich console
console = Console()

class TweetDuel:
    """Main TweetDuel application class"""
    
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path)
        self.ollama_client = ollama.Client(host=self.config.get('ollama_host', 'http://localhost:11434'))
        self.model = self.config.get('ai', {}).get('model', 'llama3.2')
        self.temperature = self.config.get('ai', {}).get('temperature', 0.8)
        self.max_tokens = self.config.get('ai', {}).get('max_tokens', 500)
        
        # Create directories
        self.duels_dir = Path("duels")
        self.armory_dir = Path("armory")
        self.cache_dir = Path("cache")
        
        self.reports_dir = Path(self.config.get("reports", {}).get("output_dir", "reports"))
        for directory in [self.duels_dir, self.armory_dir, self.cache_dir, self.reports_dir]:
            directory.mkdir(exist_ok=True)

        lang = self.config.get("language", "en")
        set_default_language(lang)
    
    def load_config(self, config_path: str = None) -> Dict:
        """Load configuration from file or create default"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default config
        default_config = {
            'ai': {
                'model': 'llama3.2',
                'temperature': 0.8,
                'max_tokens': 500
            },
            'scraping': {
                'max_replies': 50,
                'include_quotes': True,
                'language_filter': 'en'
            },
            'debate': {
                'default_persona': 'socrates',
                'response_styles': ['contrarian', 'devils_advocate', 'nuanced'],
                'viral_hooks': True
            },
            'ollama_host': 'http://localhost:11434'
        }
        
        # Save default config
        config_file = Path.home() / '.tweetduel' / 'config.yaml'
        config_file.parent.mkdir(exist_ok=True)
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        return default_config
    
    def extract_tweet_id(self, url: str) -> str:
        """Extract tweet ID from Twitter URL"""
        try:
            # Handle various Twitter URL formats
            if '/status/' in url:
                tweet_id = url.split('/status/')[1].split('?')[0]
                return tweet_id
            else:
                raise ValueError("Invalid Twitter URL format")
        except Exception as e:
            console.print(f"[red]{t('error_extracting_id', e=e)}[/red]")
            return None
    
    def scrape_tweet(self, tweet_id: str) -> Dict:
        """Scrape tweet and replies using snscrape"""
        console.print(f"[yellow]🥊 {t('scraping')}[/yellow]")
        
        try:
            # Scrape the main tweet
            tweet_data = None
            for tweet in sntwitter.TwitterTweetScraper(tweet_id).get_items():
                tweet_data = {
                    'id': tweet.id,
                    'url': tweet.url,
                    'content': tweet.rawContent,
                    'author': tweet.user.username,
                    'date': tweet.date.isoformat(),
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'replies': tweet.replyCount
                }
                break
            
            if not tweet_data:
                raise Exception("Could not scrape tweet")
            
            # Scrape replies
            replies = []
            max_replies = self.config['scraping']['max_replies']
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Scraping replies...", total=max_replies)
                
                for reply in sntwitter.TwitterTweetScraper(tweet_id).get_items():
                    if len(replies) >= max_replies:
                        break
                    
                    if hasattr(reply, 'inReplyToTweetId') and reply.inReplyToTweetId == tweet_id:
                        reply_data = {
                            'id': reply.id,
                            'content': reply.rawContent,
                            'author': reply.user.username,
                            'date': reply.date.isoformat(),
                            'likes': reply.likeCount,
                            'retweets': reply.retweetCount,
                            'replies': reply.replyCount
                        }
                        replies.append(reply_data)
                        progress.update(task, advance=1)
            
            return {
                'tweet': tweet_data,
                'replies': replies
            }
            
        except Exception as e:
            console.print(f"[red]{t('error_scraping', e=e)}[/red]")
            return None
    
    def analyze_arguments(self, content: str) -> Dict:
        """Analyze arguments in tweet/reply content"""
        prompt = f"""
        Analyze the following text and identify:
        1. Main arguments/claims
        2. Logical fallacies
        3. Weak points
        4. Emotional appeals
        5. Evidence used
        
        Text: {content}
        
        Provide a structured analysis in JSON format.
        """
        
        try:
            response = self.ollama_client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            
            # Try to parse JSON response
            try:
                return json.loads(response['response'])
            except:
                # If not valid JSON, return structured text
                return {
                    'analysis': response['response'],
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            console.print(f"[red]{t('error_analyzing', e=e)}[/red]")
            return {'error': str(e)}
    
    def generate_counter_response(self, original_content: str, analysis: Dict, persona: str = 'socrates') -> Dict:
        """Generate counter-response using specified persona"""
        personas = {
            'socrates': "You are Socrates. Use Socratic questioning to challenge assumptions. Ask probing questions that expose logical gaps.",
            'machiavelli': "You are Machiavelli. Be strategic and provocative. Use psychological manipulation and strategic thinking.",
            'chomsky': "You are Noam Chomsky. Be academic and evidence-based. Focus on systemic analysis and factual accuracy.",
            'tate': "You are Andrew Tate. Be aggressive and dominant. Use strong language and challenge authority.",
            'neutral': "You are a neutral analyst. Be balanced and factual. Present counter-arguments respectfully."
        }
        
        persona_style = personas.get(persona, personas['neutral'])
        
        prompt = f"""
        {persona_style}
        
        Original content: {original_content}
        
        Analysis: {json.dumps(analysis, indent=2)}
        
        Generate a powerful counter-response that:
        1. Addresses the main arguments
        2. Exploits logical weaknesses
        3. Adds viral engagement hooks
        4. Maintains the {persona} style
        
        Provide the response in this format:
        - Main counter-argument
        - Supporting points
        - Engagement hook
        - Call to action
        """
        
        try:
            response = self.ollama_client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            
            return {
                'persona': persona,
                'response': response['response'],
                'timestamp': datetime.now().isoformat(),
                'model': self.model
            }
            
        except Exception as e:
            console.print(f"[red]{t('error_generating', e=e)}[/red]")
            return {'error': str(e)}
    
    def create_duel_summary(self, tweet_data: Dict, replies: List, counters: List) -> str:
        """Create a summary of the duel"""
        summary = f"""
# TweetDuel Summary 🥊💬

## Original Tweet
**Author:** @{tweet_data['author']}
**Content:** {tweet_data['content']}
**Engagement:** {tweet_data['likes']} likes, {tweet_data['retweets']} retweets, {tweet_data['replies']} replies

## Replies Analyzed: {len(replies)}

## Counter-Responses Generated: {len(counters)}

## Duel Statistics
- **Total Arguments:** {len(replies)}
- **Personas Used:** {len(set(c['persona'] for c in counters if 'persona' in c))}
- **AI Model:** {self.model}
- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*Generated by TweetDuel - The AI Debate Champion*
        """
        return summary
    
    def save_duel(self, tweet_data: Dict, replies: List, counters: List, duel_id: str, thread_prediction: Optional[Dict] = None):
        """Save duel data to file"""
        duel_data = {
            'duel_id': duel_id,
            'timestamp': datetime.now().isoformat(),
            'tweet': tweet_data,
            'replies': replies,
            'counters': counters,
            'summary': self.create_duel_summary(tweet_data, replies, counters),
            'thread_prediction': thread_prediction,
        }
        
        duel_file = self.duels_dir / f"{duel_id}.json"
        with open(duel_file, 'w') as f:
            json.dump(duel_data, f, indent=2)
        
        console.print(f"[green]💾 {t('duel_saved', path=duel_file)}[/green]")
    
    def display_results(self, tweet_data: Dict, replies: List, counters: List):
        """Display duel results in a beautiful format"""
        console.print("\n" + "="*80)
        console.print(Panel.fit("🥊 TWEETDUEL RESULTS 💬", style="bold blue"))
        console.print("="*80)
        
        # Original tweet
        console.print(Panel(
            f"[bold]@{tweet_data['author']}[/bold]\n\n{tweet_data['content']}\n\n"
            f"❤️ {tweet_data['likes']} | 🔄 {tweet_data['retweets']} | 💬 {tweet_data['replies']}",
            title="🎯 Original Tweet",
            style="green"
        ))
        
        # Replies and counters
        for i, (reply, counter) in enumerate(zip(replies, counters)):
            console.print(f"\n[bold cyan]Reply #{i+1}[/bold]")
            console.print(Panel(
                f"[bold]@{reply['author']}[/bold]\n\n{reply['content']}\n\n"
                f"❤️ {reply['likes']} | 🔄 {reply['retweets']}",
                title="💬 Reply",
                style="yellow"
            ))
            
            if 'error' not in counter:
                console.print(Panel(
                    f"[bold]{counter['persona'].upper()}[/bold] Response:\n\n{counter['response']}",
                    title="⚔️ Counter-Attack",
                    style="red"
                ))
            else:
                console.print(f"[red]Error generating counter: {counter['error']}[/red]")
        
        console.print("\n" + "="*80)
    
    def _generate_and_save_report(
        self, tweet_data: Dict, replies: List, counters: List,
        thread_prediction: Optional[Dict], report_format: str, report_out: Optional[str], duel_id: str,
    ):
        out_dir = self.reports_dir
        if not report_out:
            report_out = str(out_dir / f"report_{duel_id}.{report_format if report_format != 'html' else 'html'}")
        generate_report(
            tweet_data, replies, counters,
            thread_prediction=thread_prediction,
            format=report_format,
            output_path=report_out,
        )
        console.print(f"[green]📄 {t('report_generated', path=report_out)}[/green]")

    def _offer_post_replies(self, tweet_id: str, counters: List):
        """Ask user to post one or more counter replies to Twitter."""
        client, err = get_twitter_client(self.config)
        if not client:
            console.print(f"[yellow]Twitter bot: {err}[/yellow]")
            return
        for i, c in enumerate(counters):
            if "error" in c or "response" not in c:
                continue
            text = (c.get("response") or "")[:280]
            if not text:
                continue
            console.print(Panel(text[:200] + ("..." if len(text) > 200 else ""), title=f"Counter {i+1} ({c.get('persona', '')})"))
            if Confirm.ask(t("post_approval")):
                ok, err_msg, _ = post_reply(client, str(tweet_id), text, self.config)
                if ok:
                    console.print(f"[green]{t('post_success')}[/green]")
                else:
                    console.print(f"[red]{err_msg}[/red]")
            else:
                console.print(f"[dim]{t('post_cancelled')}[/dim]")

    def run_instant_duel(self, tweet_url: str, persona: str = None):
        """Run instant duel mode"""
        console.print(f"[bold blue]🥊 {t('instant_mode')}[/bold blue]")
        
        # Extract tweet ID
        tweet_id = self.extract_tweet_id(tweet_url)
        if not tweet_id:
            return
        
        # Scrape tweet and replies
        data = self.scrape_tweet(tweet_id)
        if not data:
            return
        
        tweet_data = data['tweet']
        replies = data['replies']
        
        if not replies:
            console.print(f"[yellow]{t('no_replies')}[/yellow]")
            return
        
        # Analyze and generate counters
        console.print(f"[yellow]🧠 {t('analyzing', count=len(replies))}[/yellow]")
        counters = []
        
        for i, reply in enumerate(replies):
            console.print(f"[cyan]{t('analyzing_reply', current=i+1, total=len(replies))}[/cyan]")
            
            # Analyze arguments
            analysis = self.analyze_arguments(reply['content'])
            
            # Generate counter
            persona_to_use = persona or self.config['debate']['default_persona']
            counter = self.generate_counter_response(reply['content'], analysis, persona_to_use)
            counters.append(counter)
        
        # Display results
        self.display_results(tweet_data, replies, counters)
        
        # Thread prediction (before save so we store it)
        thread_prediction = self.run_thread_prediction(tweet_data, replies)
        if thread_prediction and "error" not in thread_prediction:
            self._display_thread_prediction(thread_prediction)
        
        # Save duel
        duel_id = f"duel_{tweet_id}_{int(time.time())}"
        self.save_duel(tweet_data, replies, counters, duel_id, thread_prediction=thread_prediction)

        # Report generation
        if getattr(self, "_report_format", None):
            self._generate_and_save_report(
                tweet_data, replies, counters, thread_prediction,
                self._report_format, self._report_out, duel_id,
            )

        # Ask if user wants to save to armory
        if Confirm.ask(f"💾 {t('save_to_armory_prompt')}"):
            self.save_to_armory(counters, duel_id)

        # Optional: post to Twitter with approval
        if getattr(self, "_offer_post", False) and is_bot_available(self.config):
            self._offer_post_replies(tweet_data.get("id"), counters)
    
    def save_to_armory(self, counters: List, duel_id: str):
        """Save generated responses to armory"""
        armory_file = self.armory_dir / f"{duel_id}_armory.json"
        
        armory_data = {
            'duel_id': duel_id,
            'timestamp': datetime.now().isoformat(),
            'responses': counters,
            'deployed': False
        }
        
        with open(armory_file, 'w') as f:
            json.dump(armory_data, f, indent=2)
        
        console.print(f"[green]💾 {t('armory_saved', path=armory_file)}[/green]")
    
    def run_thread_prediction(self, tweet_data: Dict, replies: List, horizon: str = "short") -> Optional[Dict]:
        """Run AI thread prediction. Returns prediction dict or None."""
        from utils.ai_analyzer import AIAnalyzer
        lang = self.config.get("language", "en")
        analyzer = AIAnalyzer(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return analyzer.predict_thread_direction(tweet_data, replies, horizon=horizon, language_hint=lang)

    def _display_thread_prediction(self, prediction: Dict):
        """Display thread prediction in terminal."""
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]{t('thread_prediction')}[/bold cyan]",
            style="cyan",
        ))
        summary = prediction.get("summary") or prediction.get("analysis") or json.dumps(prediction, indent=2)[:800]
        console.print(Panel(summary, title=t("prediction_title"), style="dim"))
        if prediction.get("likely_directions"):
            console.print("[dim]Likely directions: " + ", ".join(prediction.get("likely_directions", [])) + "[/dim]")

    def run_sniper_mode(self, tweet_url: str):
        """Run sniper mode - wait for new replies"""
        console.print(f"[bold blue]🎯 {t('sniper_mode')}[/bold blue]")
        console.print(t("sniper_watching"))
        
        # This would implement real-time monitoring
        # For now, just show the concept
        console.print(f"[yellow]{t('sniper_concept')}[/yellow]")
    
    def run_armory_mode(self, tweet_url: str):
        """Run armory mode - save all responses"""
        console.print(f"[bold blue]💾 {t('armory_mode')}[/bold blue]")
        console.print(t("armory_generating"))
        
        # Run instant duel first
        self.run_instant_duel(tweet_url)
        
        console.print(f"[green]{t('armory_done')}[/green]")

@click.command()
@click.option('--url', '-u', help='Tweet URL to duel')
@click.option('--mode', '-m',
              type=click.Choice(['instant', 'sniper', 'armory']),
              default='instant',
              help='Duel mode')
@click.option('--persona', '-p',
              type=click.Choice(['socrates', 'machiavelli', 'chomsky', 'tate', 'neutral']),
              help='Debate persona to use')
@click.option('--config', '-c', help='Path to config file')
@click.option('--lang', '-l', 'language',
              type=click.Choice(get_supported_languages()),
              help='UI/output language (en, tr, es, de, fr)')
@click.option('--report', '-r', 'report_format',
              type=click.Choice(['html', 'text', 'json']),
              help='Generate report after duel (html, text, json)')
@click.option('--report-out', help='Report output path (default: reports/report_<duel_id>.<ext>)')
@click.option('--post', 'offer_post', is_flag=True, help='Offer to post counter-replies to Twitter (with approval)')
@click.option('--batch', '-b', 'batch_file', help='Batch process: file with one tweet URL per line')
@click.option('--stats', is_flag=True, help='Show duel and armory stats')
@click.option('--export', 'export_format', type=click.Choice(['md', 'json']), help='Export last duel to markdown or JSON')
@click.option('--predict-only', is_flag=True, help='Only run thread prediction for the given URL (no counters)')
def main(url, mode, persona, config, language, report_format, report_out, offer_post, batch_file, stats, export_format, predict_only):
    """TweetDuel - AI-powered Twitter debate tool"""
    
    # Show banner
    console.print(Panel.fit(
        "[bold blue]🥊 TweetDuel 💬[/bold blue]\n"
        "[italic]The AI Debate Champion[/italic]",
        style="bold blue"
    ))
    
    try:
        # Initialize TweetDuel
        tweetduel = TweetDuel(config)
        if language:
            set_default_language(language)
        
        # Stats only
        if stats:
            from utils.tools import get_duel_stats
            s = get_duel_stats(tweetduel.duels_dir, tweetduel.armory_dir)
            console.print(f"[cyan]{t('stats_duels', count=s['total_duels'])}[/cyan]")
            console.print(f"[cyan]{t('stats_armory', count=s['total_armory_items'])}[/cyan]")
            if s.get("last_duel_at"):
                console.print(f"[dim]Last duel: {s['last_duel_at']}[/dim]")
            return
        
        # Export last duel
        if export_format:
            from utils.tools import list_duel_files, load_duel, export_duel_markdown, export_duel_json
            files = list_duel_files(tweetduel.duels_dir)
            if not files:
                console.print("[yellow]No duels found. Run a duel first.[/yellow]")
                return
            duel_data = load_duel(files[0])
            if not duel_data:
                console.print("[red]Could not load duel.[/red]")
                return
            tdata, replies, counters = duel_data["tweet"], duel_data["replies"], duel_data["counters"]
            pred = duel_data.get("thread_prediction")
            out = str(tweetduel.reports_dir / f"export_{files[0].replace('.json','').split(os.sep)[-1]}.{'md' if export_format == 'md' else 'json'}")
            if export_format == "md":
                export_duel_markdown(tdata, replies, counters, out, pred)
            else:
                export_duel_json(tdata, replies, counters, out, pred)
            console.print(f"[green]Exported to {out}[/green]")
            return
        
        # Predict-only mode
        if predict_only:
            if not url:
                url = Prompt.ask(f"🔗 {t('enter_tweet_url')}")
            if not url:
                console.print(f"[red]{t('no_url')}[/red]")
                return
            tid = tweetduel.extract_tweet_id(url)
            if not tid:
                return
            data = tweetduel.scrape_tweet(tid)
            if not data:
                return
            pred = tweetduel.run_thread_prediction(data["tweet"], data["replies"])
            if pred and "error" not in pred:
                tweetduel._display_thread_prediction(pred)
            else:
                console.print("[red]Prediction failed.[/red]")
            return
        
        # Batch mode
        if batch_file:
            if not os.path.exists(batch_file):
                console.print(f"[red]File not found: {batch_file}[/red]")
                return
            with open(batch_file, "r") as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            console.print(f"[yellow]{t('batch_processing', count=len(urls))}[/yellow]")
            for u in urls:
                tweetduel.run_instant_duel(u, persona)
            return
        
        # Check if Ollama is running
        try:
            models = tweetduel.ollama_client.list()
            model_names = [m['name'] for m in models.get('models', [])]
            console.print(f"[green]✅ {t('ollama_connected', models=model_names)}[/green]")
        except Exception as e:
            console.print(f"[red]❌ {t('ollama_not_running')}[/red]")
            console.print("[yellow]curl https://ollama.ai/install.sh | sh[/yellow]")
            console.print("[yellow]ollama serve[/yellow]")
            return
        
        # Get tweet URL if not provided
        if not url:
            url = Prompt.ask(f"🔗 {t('enter_tweet_url')}")
        
        if not url:
            console.print(f"[red]{t('no_url')}[/red]")
            return
        
        # Wire report and post options
        tweetduel._report_format = report_format
        tweetduel._report_out = report_out
        tweetduel._offer_post = offer_post
        
        # Run selected mode
        if mode == 'instant':
            tweetduel.run_instant_duel(url, persona)
        elif mode == 'sniper':
            tweetduel.run_sniper_mode(url)
        elif mode == 'armory':
            tweetduel.run_armory_mode(url)
            
    except KeyboardInterrupt:
        console.print(f"\n[yellow]{t('interrupted')}[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print_exception()

if __name__ == "__main__":
    main()
