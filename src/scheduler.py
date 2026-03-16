"""Main entry point: pick topic, generate article, post to Reddit, log results."""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config.json"
QUEUE_PATH = ROOT / "content-queue.jsonl"
HISTORY_PATH = ROOT / "post-history.jsonl"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def load_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    topics = []
    for line in QUEUE_PATH.read_text().strip().split("\n"):
        if line.strip():
            topics.append(json.loads(line))
    return topics


def save_queue(topics: list[dict]):
    with open(QUEUE_PATH, "w") as f:
        for t in topics:
            f.write(json.dumps(t) + "\n")


def append_history(entry: dict):
    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_recent_post_count(max_hours: float) -> int:
    """Count posts within the last max_hours."""
    if not HISTORY_PATH.exists():
        return 0
    now = datetime.now(timezone.utc)
    count = 0
    for line in HISTORY_PATH.read_text().strip().split("\n"):
        if not line.strip():
            continue
        entry = json.loads(line)
        posted_at = datetime.fromisoformat(entry["timestamp"])
        hours_ago = (now - posted_at).total_seconds() / 3600
        if hours_ago <= max_hours:
            count += 1
    return count


def pick_next_topic(topics: list[dict]) -> dict | None:
    """Pick the first unposted topic."""
    for t in topics:
        if not t.get("posted", False):
            return t
    return None


def run(dry_run: bool = False, save_to: str | None = None):
    """Main scheduling loop (single execution).

    Args:
        dry_run: Generate article but don't post to Reddit
        save_to: If set, save the generated article to this file path
    """
    config = load_config()
    topics = load_queue()

    if not topics:
        print("No topics in queue. Run seed_topics.py first.")
        sys.exit(1)

    topic = pick_next_topic(topics)
    if topic is None:
        print("All topics have been posted. Regenerate with seed_topics.py.")
        sys.exit(0)

    # Check posting limits
    if not dry_run:
        posting = config["posting"]
        if not posting["enabled"]:
            print("Posting is disabled in config. Set posting.enabled=true or use --dry-run.")
            sys.exit(1)

        recent = get_recent_post_count(24)
        if recent >= posting["max_per_day"]:
            print(f"Already posted {recent} times today (max: {posting['max_per_day']}). Skipping.")
            sys.exit(0)

    # Generate article
    from src.generate import generate_article

    print(f"Generating article: {topic['title']}")
    gen_config = {**config["generation"], **config.get("content", {})}
    article = generate_article(topic, gen_config)
    print(f"Generated {len(article['body'])} chars")

    if save_to:
        Path(save_to).parent.mkdir(parents=True, exist_ok=True)
        with open(save_to, "w") as f:
            f.write(f"# {article['title']}\n\n{article['body']}\n")
        print(f"Saved to {save_to}")

    # Post to Reddit
    url = None
    status = "dry_run"
    if not dry_run:
        from src.post import submit_post

        print(f"Posting to r/{config['subreddit']}...")
        url = submit_post(article["title"], article["body"], config["subreddit"])
        status = "posted"
        print(f"Posted: {url}")

    # Log to history
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "topic_id": topic["id"],
        "title": topic["title"],
        "pillar": topic["pillar"],
        "url": url,
        "status": status,
        "chars": len(article["body"]),
    }
    append_history(entry)

    # Mark topic as posted
    for t in topics:
        if t["id"] == topic["id"]:
            t["posted"] = True
            break
    save_queue(topics)

    print("Done.")
    return article


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or os.environ.get("DRY_RUN", "").lower() in ("1", "true")
    save = None
    for i, arg in enumerate(sys.argv):
        if arg == "--save-to" and i + 1 < len(sys.argv):
            save = sys.argv[i + 1]
    run(dry_run=dry, save_to=save)
