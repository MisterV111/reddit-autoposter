"""Send caller-aware notification for human review of content variants.

Routes notifications to the correct agent session via ~/bin/tell-agent,
falling back to stdout if the script is not found.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

VALID_CALLERS = ("main", "dev", "reel", "pixel", "buzz", "scout", "reach", "forge")
TELL_AGENT = Path.home() / "bin" / "tell-agent"


def build_message(topic, variants, winner, slop_score, char_counts=None):
    """Build the review notification message."""
    lines = [
        "New content ready for review.",
        "",
        f"Topic: {topic}",
        f"Winner: Variant {winner} (score: {slop_score})",
        "",
    ]

    for label, info in variants.items():
        lines.append(f"  {label}: {info}")

    lines.append("")

    # Platform format options with char counts
    if char_counts:
        rc = char_counts.get("reddit_post", "?")
        lpc = char_counts.get("linkedin_post", "?")
        lac = char_counts.get("linkedin_article", "?")
        xpc = char_counts.get("x_post", "?")
        xac = char_counts.get("x_article", "?")

        lines.append(f"Reddit: Post ({rc} chars)")
        lines.append(f"LinkedIn: Post ({lpc} chars) or Article ({lac} chars)")
        lines.append(f"X: Post ({xpc} chars) or Article ({xac} chars)")
        lines.append("")

    lines.extend([
        "Reply with your picks per platform:",
        "Example: reddit, linkedin article, x post",
        "Or: all articles",
        "Or: all posts",
        "Or: SKIP",
    ])

    return "\n".join(lines)


def send_to_agent(caller, message):
    """Route message to the caller's agent session via tell-agent."""
    if not TELL_AGENT.exists():
        return False

    try:
        subprocess.run(
            [str(TELL_AGENT), caller, message],
            check=True,
            timeout=15,
            capture_output=True,
        )
        return True
    except (subprocess.SubprocessError, OSError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Notify for content review")
    parser.add_argument("--topic", required=True, help="Topic name")
    parser.add_argument("--variant-a", required=True, help="Variant A angle and score")
    parser.add_argument("--variant-b", required=True, help="Variant B angle and score")
    parser.add_argument("--variant-c", required=True, help="Variant C angle and score")
    parser.add_argument("--winner", required=True, help="System-selected winner (A/B/C)")
    parser.add_argument("--slop-score", required=True, help="Stop-slop score")
    parser.add_argument("--caller", default="main", choices=VALID_CALLERS,
                        help="Agent session to route notification to (default: main)")
    parser.add_argument("--run-id", default=None, help="Run ID for reference")
    parser.add_argument("--reddit-post-chars", type=int, default=None, help="Reddit post char count")
    parser.add_argument("--linkedin-post-chars", type=int, default=None, help="LinkedIn post char count")
    parser.add_argument("--linkedin-article-chars", type=int, default=None, help="LinkedIn article char count")
    parser.add_argument("--x-post-chars", type=int, default=None, help="X post char count")
    parser.add_argument("--x-article-chars", type=int, default=None, help="X article char count")
    args = parser.parse_args()

    variants = {
        "A": args.variant_a,
        "B": args.variant_b,
        "C": args.variant_c,
    }

    char_counts = None
    if args.reddit_post_chars is not None:
        char_counts = {
            "reddit_post": args.reddit_post_chars,
            "linkedin_post": args.linkedin_post_chars or "?",
            "linkedin_article": args.linkedin_article_chars or "?",
            "x_post": args.x_post_chars or "?",
            "x_article": args.x_article_chars or "?",
        }

    message = build_message(args.topic, variants, args.winner, args.slop_score, char_counts)

    if args.run_id:
        message += f"\n\nRun ID: {args.run_id}"

    if send_to_agent(args.caller, message):
        print(f"Notification routed to agent: {args.caller}")
    else:
        print(f"tell-agent not available. Printing summary to stdout:\n")
        print(message)


if __name__ == "__main__":
    main()
