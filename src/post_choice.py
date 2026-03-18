"""Post Juan's chosen variant to all platforms."""

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

# Add src to path so post_all imports work
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def load_metadata(run_id):
    """Load metadata.json for a given run ID."""
    meta_path = REVIEW_DIR / run_id / "metadata.json"
    if not meta_path.exists():
        print(f"Error: no review data found for run {run_id}", file=sys.stderr)
        print(f"Expected: {meta_path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(meta_path.read_text())


def load_variant_files(run_id, choice):
    """Load the 3 platform files for the chosen variant."""
    variant_dir = REVIEW_DIR / run_id
    prefix = choice.upper()

    files = {}
    for platform in ["reddit", "linkedin", "x"]:
        path = variant_dir / f"{prefix}_{platform}.md"
        if not path.exists():
            print(f"Error: missing {path}", file=sys.stderr)
            sys.exit(1)
        files[platform] = path.read_text().strip()

    return files


def log_preference(metadata, choice):
    """Append preference data to preference-log.jsonl."""
    system_winner = metadata.get("winner", "?")

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": metadata.get("run_id", "?"),
        "topic": metadata.get("topic", "?"),
        "system_winner": system_winner,
        "juan_choice": choice.upper(),
        "system_score": metadata.get("scores", {}).get(system_winner, None),
        "match": choice.upper() == system_winner.upper(),
        "platforms": ["reddit", "linkedin", "x"],
    }

    with open(PREF_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"Logged preference: Juan chose {choice.upper()}, system said {system_winner} ({'match' if entry['match'] else 'override'})")


def post_variant(metadata, files):
    """Post chosen variant to all platforms via post_all.py."""
    from post_all import main as post_all_main

    title = metadata.get("title", metadata.get("topic", "Untitled"))
    subreddit = metadata.get("subreddit", "AIProductionHouse")

    # Build sys.argv for post_all
    sys.argv = [
        "post_all.py",
        "--title", title,
        "--reddit-body", files["reddit"],
        "--linkedin-body", files["linkedin"],
        "--x-body", files["x"],
        "--subreddit", subreddit,
    ]

    flair = metadata.get("flair")
    if flair:
        sys.argv.extend(["--flair", flair])

    post_all_main()


def main():
    parser = argparse.ArgumentParser(description="Post Juan's chosen content variant")
    parser.add_argument("--choice", required=True, choices=["A", "B", "C", "a", "b", "c"],
                        help="Chosen variant (A, B, or C)")
    parser.add_argument("--run-id", required=True, help="Run ID from data/review/")
    args = parser.parse_args()

    choice = args.choice.upper()

    metadata = load_metadata(args.run_id)
    files = load_variant_files(args.run_id, choice)

    log_preference(metadata, choice)

    print(f"\nPosting variant {choice} to all platforms...")
    post_variant(metadata, files)


if __name__ == "__main__":
    main()
