"""Send Telegram notification for human review of content variants."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Load .env manually (no external deps)
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def load_env():
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def build_message(topic, variants, winner, slop_score):
    """Build the review notification message."""
    lines = [
        f"📝 NEW CONTENT READY FOR REVIEW",
        f"",
        f"Topic: {topic}",
        f"",
    ]

    for label, info in variants.items():
        lines.append(f"  {label}: {info}")

    lines.extend([
        f"",
        f"System winner: {winner}",
        f"Stop-slop score: {slop_score}",
        f"",
        f"Reply A, B, or C to approve that variant.",
        f"Reply SKIP to skip this topic.",
    ])

    return "\n".join(lines)


def send_telegram(chat_id, message, gateway_url="http://localhost:18789"):
    """Send message via OpenClaw Telegram gateway."""
    payload = json.dumps({
        "chat_id": chat_id,
        "text": message,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{gateway_url}/send",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except (urllib.error.URLError, OSError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Notify Juan for content review")
    parser.add_argument("--topic", required=True, help="Topic name")
    parser.add_argument("--variant-a", required=True, help="Variant A angle and score")
    parser.add_argument("--variant-b", required=True, help="Variant B angle and score")
    parser.add_argument("--variant-c", required=True, help="Variant C angle and score")
    parser.add_argument("--winner", required=True, help="System-selected winner (A/B/C)")
    parser.add_argument("--slop-score", required=True, help="Stop-slop score")
    parser.add_argument("--run-id", default=None, help="Run ID for reference")
    args = parser.parse_args()

    load_env()

    variants = {
        "A": args.variant_a,
        "B": args.variant_b,
        "C": args.variant_c,
    }

    message = build_message(args.topic, variants, args.winner, args.slop_score)

    if args.run_id:
        message += f"\n\nRun ID: {args.run_id}"

    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "8106220540")

    if send_telegram(chat_id, message):
        print(f"Notification sent to Telegram (chat {chat_id})")
    else:
        print("Telegram gateway unavailable. Printing summary to stdout:\n")
        print(message)


if __name__ == "__main__":
    main()
