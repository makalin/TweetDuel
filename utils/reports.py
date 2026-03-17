"""
Report generation for TweetDuel (HTML, text, JSON).
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


def _escape_html(s: str) -> str:
    if not s:
        return ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def generate_html_report(
    tweet_data: Dict,
    replies: List[Dict],
    counters: List[Dict],
    thread_prediction: Optional[Dict] = None,
    output_path: Optional[str] = None,
    title: str = "TweetDuel Report",
) -> str:
    """Generate an HTML report of the duel. Returns HTML string; optionally writes to output_path."""
    rows = []
    for i, (reply, counter) in enumerate(zip(replies, counters)):
        reply_content = _escape_html(reply.get("content", ""))
        author = _escape_html(reply.get("author", ""))
        persona = counter.get("persona", "unknown")
        response = _escape_html(counter.get("response", counter.get("error", "")))
        rows.append(
            f"""
        <tr>
          <td>{i + 1}</td>
          <td><strong>@{author}</strong><br><pre>{reply_content}</pre></td>
          <td><strong>{persona}</strong><br><pre>{response}</pre></td>
        </tr>"""
        )

    prediction_html = ""
    if thread_prediction and "error" not in thread_prediction:
        pred = thread_prediction
        summary = _escape_html(
            pred.get("summary") or pred.get("analysis") or json.dumps(pred)[:500]
        )
        prediction_html = f"""
      <section class="prediction">
        <h2>Thread prediction</h2>
        <div class="prediction-content"><pre>{summary}</pre></div>
      </section>"""

    original_content = _escape_html(tweet_data.get("content", ""))
    original_author = _escape_html(tweet_data.get("author", ""))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_escape_html(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 0 auto; padding: 1rem; background: #1a1a2e; color: #eee; }}
    h1 {{ color: #00d4ff; }}
    h2 {{ color: #0f3460; margin-top: 2rem; }}
    .meta {{ color: #888; font-size: 0.9rem; margin-bottom: 1.5rem; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
    th, td {{ border: 1px solid #333; padding: 0.75rem; text-align: left; vertical-align: top; }}
    th {{ background: #16213e; color: #00d4ff; }}
    tr:nth-child(even) {{ background: #0f0f23; }}
    pre {{ white-space: pre-wrap; word-break: break-word; margin: 0; font-size: 0.9rem; }}
    .original {{ background: #0f3460; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; }}
    .prediction {{ background: #16213e; padding: 1rem; border-radius: 8px; }}
    .prediction-content pre {{ color: #a0a0a0; }}
  </style>
</head>
<body>
  <h1>TweetDuel Report</h1>
  <div class="meta">Generated {datetime.now().strftime("%Y-%m-%d %H:%M")} | Replies: {len(replies)} | Counters: {len(counters)}</div>

  <section class="original">
    <h2>Original tweet</h2>
    <p><strong>@{original_author}</strong></p>
    <pre>{original_content}</pre>
    <p class="meta">Likes: {tweet_data.get("likes", 0)} | Retweets: {tweet_data.get("retweets", 0)} | Replies: {tweet_data.get("replies", 0)}</p>
  </section>

  <h2>Replies &amp; counter-responses</h2>
  <table>
    <thead><tr><th>#</th><th>Reply</th><th>Counter (persona)</th></tr></thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
  {prediction_html}
</body>
</html>"""

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
    return html


def generate_text_report(
    tweet_data: Dict,
    replies: List[Dict],
    counters: List[Dict],
    thread_prediction: Optional[Dict] = None,
    output_path: Optional[str] = None,
) -> str:
    """Generate a plain text report. Returns content; optionally writes to output_path."""
    lines = [
        "=" * 60,
        "TweetDuel Report",
        "=" * 60,
        "",
        "Original tweet",
        "-" * 40,
        f"@{tweet_data.get('author', '')}",
        tweet_data.get("content", ""),
        f"Likes: {tweet_data.get('likes', 0)} | Retweets: {tweet_data.get('retweets', 0)} | Replies: {tweet_data.get('replies', 0)}",
        "",
    ]
    for i, (reply, counter) in enumerate(zip(replies, counters)):
        lines.extend(
            [
                f"Reply #{i + 1}",
                "-" * 40,
                f"@{reply.get('author', '')}",
                reply.get("content", ""),
                "",
                f"Counter ({counter.get('persona', 'unknown')})",
                counter.get("response", counter.get("error", "")),
                "",
            ]
        )
    if thread_prediction and "error" not in thread_prediction:
        lines.extend(
            [
                "Thread prediction",
                "-" * 40,
                thread_prediction.get("summary") or str(thread_prediction.get("analysis", "")),
                "",
            ]
        )
    lines.append("=" * 60)
    text = "\n".join(lines)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
    return text


def generate_report(
    tweet_data: Dict,
    replies: List[Dict],
    counters: List[Dict],
    thread_prediction: Optional[Dict] = None,
    format: str = "html",
    output_path: Optional[str] = None,
) -> str:
    """Generate report in format: 'html', 'text', or 'json'. Returns content."""
    if format == "json":
        data = {
            "generated_at": datetime.now().isoformat(),
            "tweet": tweet_data,
            "replies": replies,
            "counters": counters,
            "thread_prediction": thread_prediction,
        }
        content = json.dumps(data, indent=2, ensure_ascii=False)
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
        return content
    if format == "text":
        return generate_text_report(
            tweet_data, replies, counters, thread_prediction, output_path
        )
    return generate_html_report(
        tweet_data, replies, counters, thread_prediction, output_path, "TweetDuel Report"
    )
