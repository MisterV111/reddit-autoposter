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


def build_message(topic, variants, winner, slop_score):
    """Build the review notification message."""
    lines = [
        "📝 NEW CONTENT READY FOR REVIEW",
        "",
        f"Topic: {topic}",
        "",
    ]

    for label, info in variants.items():
        lines.append(f"  {label}: {info}")

    lines.extend([
        "",
        f"System winner: {winner}",
        f"Stop-slop score: {slop_score}",
        "",
        "Reply A, B, or C to approve that variant.",
        "Reply SKIP to skip this topic.",
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
    args = parser.parse_args()

    variants = {
        "A": args.variant_a,
        "B": args.variant_b,
        "C": args.variant_c,
    }

    message = build_message(args.topic, variants, args.winner, args.slop_score)

    if args.run_id:
        message += f"\n\nRun ID: {args.run_id}"

    if send_to_agent(args.caller, message):
        print(f"Notification routed to agent: {args.caller}")
    else:
        print(f"tell-agent not available. Printing summary to stdout:\n")
        print(message)


if __name__ == "__main__":
    main()
