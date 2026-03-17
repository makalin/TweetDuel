"""
Extra tools: export, batch processing, stats.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


def export_duel_markdown(
    tweet_data: Dict,
    replies: List[Dict],
    counters: List[Dict],
    output_path: str,
    include_prediction: Optional[Dict] = None,
) -> str:
    """Export duel to a Markdown file. Returns path."""
    lines = [
        "# TweetDuel Export",
        "",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Original Tweet",
        f"- **@{tweet_data.get('author', '')}**",
        f"- {tweet_data.get('content', '')}",
        f"- Likes: {tweet_data.get('likes', 0)} | RT: {tweet_data.get('retweets', 0)} | Replies: {tweet_data.get('replies', 0)}",
        "",
        "## Replies & Counters",
        "",
    ]
    for i, (reply, counter) in enumerate(zip(replies, counters)):
        lines.append(f"### {i + 1}. @{reply.get('author', '')}")
        lines.append("")
        lines.append(reply.get("content", ""))
        lines.append("")
        lines.append(f"**Counter ({counter.get('persona', '')}):**")
        lines.append("")
        lines.append(counter.get("response", counter.get("error", "")))
        lines.append("")
    if include_prediction and "error" not in include_prediction:
        lines.append("## Thread Prediction")
        lines.append("")
        lines.append(include_prediction.get("summary") or str(include_prediction.get("analysis", "")))
        lines.append("")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def export_duel_json(
    tweet_data: Dict,
    replies: List[Dict],
    counters: List[Dict],
    output_path: str,
    include_prediction: Optional[Dict] = None,
) -> str:
    """Export duel to JSON. Returns path."""
    data = {
        "exported_at": datetime.now().isoformat(),
        "tweet": tweet_data,
        "replies": replies,
        "counters": counters,
        "thread_prediction": include_prediction,
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return str(path)


def get_duel_stats(duels_dir: Optional[Path] = None, armory_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Return stats: total duels, total armory items, last duel time, etc."""
    duels_dir = duels_dir or Path("duels")
    armory_dir = armory_dir or Path("armory")
    stats = {
        "total_duels": 0,
        "total_armory_items": 0,
        "last_duel_at": None,
        "duel_ids": [],
        "armory_ids": [],
    }
    if duels_dir.exists():
        files = list(duels_dir.glob("*.json"))
        stats["total_duels"] = len(files)
        stats["duel_ids"] = [f.stem for f in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:20]]
        if files:
            latest = max(files, key=lambda p: p.stat().st_mtime)
            stats["last_duel_at"] = datetime.fromtimestamp(latest.stat().st_mtime).isoformat()
    if armory_dir.exists():
        files = list(armory_dir.glob("*.json"))
        stats["total_armory_items"] = len(files)
        stats["armory_ids"] = [f.stem for f in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:20]]
    return stats


def load_duel(duel_path: str) -> Optional[Dict[str, Any]]:
    """Load a duel JSON file. Returns dict or None."""
    path = Path(duel_path)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def list_duel_files(duels_dir: Optional[Path] = None) -> List[str]:
    """List paths of duel JSON files, newest first."""
    duels_dir = duels_dir or Path("duels")
    if not duels_dir.exists():
        return []
    files = sorted(duels_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(f) for f in files]


def list_armory_files(armory_dir: Optional[Path] = None) -> List[str]:
    """List paths of armory JSON files, newest first."""
    armory_dir = armory_dir or Path("armory")
    if not armory_dir.exists():
        return []
    files = sorted(armory_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(f) for f in files]
