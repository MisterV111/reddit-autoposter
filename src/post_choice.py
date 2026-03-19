"""Post Juan's chosen variant to all platforms with per-platform format selection."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REVIEW_DIR = DATA_DIR / "review"
PREF_LOG = DATA_DIR / "preference-log.jsonl"

# Add src to path so post imports work
sys.path.insert(0, str(PROJECT_ROOT / "src"))

VALID_FORMATS = ("post", "article", "skip", "both")


def load_metadata(run_id):
    """Load metadata.json for a given run ID."""
    meta_path = REVIEW_DIR / run_id / "metadata.json"
    if not meta_path.exists():
        print(f"Error: no review data found for run {run_id}", file=sys.stderr)
        print(f"Expected: {meta_path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(meta_path.read_text())


def load_format_file(run_id, filename):
    """Load a specific format file from the review directory."""
    path = REVIEW_DIR / run_id / filename
    if not path.exists():
        print(f"Error: missing {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text().strip()


def resolve_choices(args):
    """Resolve per-platform choices from args, handling --all shortcut."""
    if args.all:
        shortcut = args.all.lower().rstrip("s")  # "articles" -> "article", "posts" -> "post"
        reddit = "post"  # Reddit only has post format
        linkedin = shortcut
        x = shortcut
    else:
        reddit = (args.reddit or "post").lower()
        linkedin = (args.linkedin or "post").lower()
        x = (args.x or "post").lower()

    return {"reddit": reddit, "linkedin": linkedin, "x": x}


def log_preference(metadata, choices):
    """Append preference data to preference-log.jsonl."""
    system_winner = metadata.get("winner", "?")

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": metadata.get("run_id", "?"),
        "topic": metadata.get("topic", "?"),
        "system_winner": system_winner,
        "system_score": metadata.get("scores", {}).get(system_winner, None),
        "choices": choices,
        "platforms_posted": [p for p, fmt in choices.items() if fmt != "skip"],
    }

    with open(PREF_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    posted = [f"{p}:{fmt}" for p, fmt in choices.items() if fmt != "skip"]
    skipped = [p for p, fmt in choices.items() if fmt == "skip"]
    print(f"Logged preference: {', '.join(posted)}")
    if skipped:
        print(f"Skipped: {', '.join(skipped)}")


def post_platforms(metadata, run_id, choices):
    """Post to each platform based on format choices."""
    title = metadata.get("title", metadata.get("topic", "Untitled"))
    subreddit = metadata.get("subreddit", "AIProductionHouse")
    flair = metadata.get("flair")
    results = {}
    failures = {}

    # Reddit (post only)
    if choices["reddit"] != "skip":
        try:
            from post_reddit import submit_post
            body = load_format_file(run_id, "reddit_post.md")
            url = submit_post(title, body, subreddit, flair)
            results["reddit"] = url
            print(f"Reddit: {url}")
        except Exception as e:
            failures["reddit"] = str(e)
            print(f"Reddit FAILED: {e}", file=sys.stderr)

    # LinkedIn
    if choices["linkedin"] != "skip":
        from post_linkedin import post_to_linkedin
        formats_to_post = []
        if choices["linkedin"] in ("post", "both"):
            formats_to_post.append(("post", False))
        if choices["linkedin"] in ("article", "both"):
            formats_to_post.append(("article", True))

        for fmt_name, is_article in formats_to_post:
            try:
                filename = f"linkedin_{fmt_name}.md"
                body = load_format_file(run_id, filename)
                url = post_to_linkedin(title, body, article=is_article)
                results[f"linkedin_{fmt_name}"] = url
                print(f"LinkedIn ({fmt_name}): {url}")
            except Exception as e:
                failures[f"linkedin_{fmt_name}"] = str(e)
                print(f"LinkedIn ({fmt_name}) FAILED: {e}", file=sys.stderr)

    # X
    if choices["x"] != "skip":
        from post_x import post_to_x
        formats_to_post = []
        if choices["x"] in ("post", "both"):
            formats_to_post.append(("post", False))
        if choices["x"] in ("article", "both"):
            formats_to_post.append(("article", True))

        for fmt_name, is_article in formats_to_post:
            try:
                filename = f"x_{fmt_name}.md"
                body = load_format_file(run_id, filename)
                url = post_to_x(title, body, article=is_article)
                results[f"x_{fmt_name}"] = url
                print(f"X ({fmt_name}): {url}")
            except Exception as e:
                failures[f"x_{fmt_name}"] = str(e)
                print(f"X ({fmt_name}) FAILED: {e}", file=sys.stderr)

    # Summary
    print(f"\n--- Summary ---")
    print(f"Posted: {', '.join(results.keys()) if results else 'none'}")
    if failures:
        print(f"Failed: {', '.join(failures.keys())}")

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": title,
        "choices": choices,
        "posted": results,
        "failed": failures,
    }
    print(f"\n{json.dumps(summary)}")

    return bool(results)


def main():
    parser = argparse.ArgumentParser(
        description="Post content with per-platform format selection",
        epilog="Examples:\n"
               "  %(prog)s --run-id RUN_ID --reddit post --linkedin article --x post\n"
               "  %(prog)s --run-id RUN_ID --all articles\n"
               "  %(prog)s --run-id RUN_ID --all posts\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run-id", required=True, help="Run ID from data/review/")
    parser.add_argument("--reddit", choices=VALID_FORMATS, default=None,
                        help="Reddit format: post or skip (default: post)")
    parser.add_argument("--linkedin", choices=VALID_FORMATS, default=None,
                        help="LinkedIn format: post, article, both, or skip")
    parser.add_argument("--x", choices=VALID_FORMATS, default=None,
                        help="X format: post, article, both, or skip")
    parser.add_argument("--all", choices=["posts", "articles"], default=None,
                        help="Shortcut: set all platforms to posts or articles")

    # Legacy support: --choice A/B/C still works (posts all as posts)
    parser.add_argument("--choice", choices=["A", "B", "C", "a", "b", "c"],
                        default=None, help="Legacy: choose variant A/B/C (posts all platforms)")
    args = parser.parse_args()

    if args.choice and not (args.reddit or args.linkedin or args.x or args.all):
        print(f"Legacy mode: --choice is deprecated. Use --reddit/--linkedin/--x instead.",
              file=sys.stderr)
        print(f"Posting variant {args.choice.upper()} as posts to all platforms.\n")

    metadata = load_metadata(args.run_id)
    choices = resolve_choices(args)
    log_preference(metadata, choices)

    print(f"\nPosting to platforms...")
    success = post_platforms(metadata, args.run_id, choices)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
