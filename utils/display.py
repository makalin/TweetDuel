"""
Display utilities for TweetDuel using Rich
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from typing import Dict, List, Any
from datetime import datetime

console = Console()

class TweetDuelDisplay:
    """Display utility class for TweetDuel"""
    
    def __init__(self):
        self.console = console
    
    def show_banner(self):
        """Display the TweetDuel banner"""
        banner = Panel.fit(
            "[bold blue]🥊 TweetDuel 💬[/bold blue]\n"
            "[italic]The AI Debate Champion[/italic]\n\n"
            "[dim]Turn Twitter threads into intellectual battlegrounds[/dim]",
            style="bold blue",
            border_style="blue"
        )
        self.console.print(banner)
    
    def show_duel_results(self, tweet_data: Dict, replies: List[Dict], counters: List[Dict]):
        """Display duel results in a beautiful format"""
        self.console.print("\n" + "="*80)
        self.console.print(Panel.fit("🥊 TWEETDUEL RESULTS 💬", style="bold blue"))
        self.console.print("="*80)
        
        # Original tweet
        self.console.print(Panel(
            f"[bold]@{tweet_data['author']}[/bold]\n\n{tweet_data['content']}\n\n"
            f"❤️ {tweet_data['likes']} | 🔄 {tweet_data['retweets']} | 💬 {tweet_data['replies']}",
            title="🎯 Original Tweet",
            style="green"
        ))
        
        # Replies and counters
        for i, (reply, counter) in enumerate(zip(replies, counters)):
            self.console.print(f"\n[bold cyan]Reply #{i+1}[/bold]")
            self.console.print(Panel(
                f"[bold]@{reply['author']}[/bold]\n\n{reply['content']}\n\n"
                f"❤️ {reply['likes']} | 🔄 {reply['retweets']}",
                title="💬 Reply",
                style="yellow"
            ))
            
            if 'error' not in counter:
                self.console.print(Panel(
                    f"[bold]{counter['persona'].upper()}[/bold] Response:\n\n{counter['response']}",
                    title="⚔️ Counter-Attack",
                    style="red"
                ))
            else:
                self.console.print(f"[red]Error generating counter: {counter['error']}[/red]")
        
        self.console.print("\n" + "="*80)
    
    def show_duel_summary(self, tweet_data: Dict, replies: List[Dict], counters: List[Dict]):
        """Display a summary of the duel"""
        summary_table = Table(title="🥊 Duel Summary")
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="magenta")
        
        summary_table.add_row("Original Author", f"@{tweet_data['author']}")
        summary_table.add_row("Tweet Engagement", f"❤️ {tweet_data['likes']} | 🔄 {tweet_data['retweets']} | 💬 {tweet_data['replies']}")
        summary_table.add_row("Replies Analyzed", str(len(replies)))
        summary_table.add_row("Counters Generated", str(len(counters)))
        summary_table.add_row("Personas Used", str(len(set(c.get('persona', 'unknown') for c in counters if 'error' not in c))))
        summary_table.add_row("Generated At", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        self.console.print(summary_table)
    
    def show_persona_selection(self) -> str:
        """Show persona selection interface"""
        personas = {
            'socrates': 'Question-based, philosophical, challenging assumptions',
            'machiavelli': 'Strategic, provocative, psychologically manipulative',
            'chomsky': 'Academic, evidence-based, systemic analysis',
            'tate': 'Aggressive, dominant, challenging authority',
            'neutral': 'Balanced, factual, respectful'
        }
        
        persona_table = Table(title="🎭 Select Debate Persona")
        persona_table.add_column("Persona", style="cyan", no_wrap=True)
        persona_table.add_column("Style", style="magenta")
        
        for persona, description in personas.items():
            persona_table.add_row(persona.title(), description)
        
        self.console.print(persona_table)
        
        return Prompt.ask(
            "Choose persona",
            choices=list(personas.keys()),
            default="socrates"
        )
    
    def show_mode_selection(self) -> str:
        """Show mode selection interface"""
        modes = {
            'instant': 'Analyze and generate responses immediately',
            'sniper': 'Wait for new replies and auto-generate counters',
            'armory': 'Save all responses for strategic deployment'
        }
        
        mode_table = Table(title="🎮 Select Duel Mode")
        mode_table.add_column("Mode", style="cyan", no_wrap=True)
        mode_table.add_column("Description", style="magenta")
        
        for mode, description in modes.items():
            mode_table.add_row(mode.title(), description)
        
        self.console.print(mode_table)
        
        return Prompt.ask(
            "Choose mode",
            choices=list(modes.keys()),
            default="instant"
        )
    
    def show_progress(self, description: str, total: int = None):
        """Show progress bar"""
        if total:
            return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            )
        else:
            return Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            )
    
    def show_armory_contents(self, armory_files: List[str]):
        """Show contents of the armory"""
        if not armory_files:
            self.console.print("[yellow]Armory is empty. No saved responses found.[/yellow]")
            return
        
        armory_table = Table(title="💾 Armory Contents")
        armory_table.add_column("File", style="cyan")
        armory_table.add_column("Size", style="magenta")
        armory_table.add_column("Modified", style="green")
        
        for file_path in armory_files:
            # This would get actual file info in a real implementation
            armory_table.add_row(file_path, "N/A", "N/A")
        
        self.console.print(armory_table)
    
    def show_config_summary(self, config: Dict[str, Any]):
        """Show configuration summary"""
        config_table = Table(title="⚙️ Configuration")
        config_table.add_column("Setting", style="cyan", no_wrap=True)
        config_table.add_column("Value", style="magenta")
        
        for section, settings in config.items():
            if isinstance(settings, dict):
                for key, value in settings.items():
                    config_table.add_row(f"{section}.{key}", str(value))
            else:
                config_table.add_row(section, str(settings))
        
        self.console.print(config_table)
    
    def show_error(self, error: str, details: str = None):
        """Show error message"""
        error_panel = Panel(
            f"[red]{error}[/red]\n\n[dim]{details or ''}[/dim]",
            title="❌ Error",
            style="red"
        )
        self.console.print(error_panel)
    
    def show_success(self, message: str, details: str = None):
        """Show success message"""
        success_panel = Panel(
            f"[green]{message}[/green]\n\n[dim]{details or ''}[/dim]",
            title="✅ Success",
            style="green"
        )
        self.console.print(success_panel)
    
    def show_warning(self, message: str, details: str = None):
        """Show warning message"""
        warning_panel = Panel(
            f"[yellow]{message}[/yellow]\n\n[dim]{details or ''}[/dim]",
            title="⚠️ Warning",
            style="yellow"
        )
        self.console.print(warning_panel)
    
    def show_help(self):
        """Show help information"""
        help_text = """
# TweetDuel Help 🥊💬

## Usage
```bash
python tweetduel.py --url "TWEET_URL" --mode instant --persona socrates
```

## Modes
- **instant**: Analyze and generate responses immediately
- **sniper**: Wait for new replies and auto-generate counters  
- **armory**: Save all responses for strategic deployment

## Personas
- **socrates**: Question-based, philosophical
- **machiavelli**: Strategic, provocative
- **chomsky**: Academic, evidence-based
- **tate**: Aggressive, dominant
- **neutral**: Balanced, factual

## Examples
```bash
# Quick duel with Socrates persona
python tweetduel.py -u "https://x.com/user/status/123" -p socrates

# Save responses to armory
python tweetduel.py -u "https://x.com/user/status/123" -m armory

# Use custom config
python tweetduel.py -u "https://x.com/user/status/123" -c config.yaml
```
        """
        
        self.console.print(Markdown(help_text))
