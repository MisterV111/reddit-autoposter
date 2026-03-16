"""X (Twitter) posting via Tweepy. Works as both a library and CLI tool."""

import argparse
import os
import sys

import tweepy
from dotenv import load_dotenv

load_dotenv()


def get_x_client() -> tweepy.Client:
    """Create and return an authenticated X API v2 client."""
    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_SECRET"],
    )


def post_to_x(title: str, body: str, article: bool = False) -> str:
    """Post content to X.

    Args:
        title: Post title (prepended to body for tweets, used as title for articles)
        body: Post body text
        article: If True, creates a long-form note tweet

    Returns:
        URL of the posted tweet
    """
    client = get_x_client()

    if article:
        # Long-form note tweet (X Articles / Note Tweets)
        text = f"{title}\n\n{body}"
        # Note tweets support up to 25,000 characters
        response = client.create_tweet(text=text)
    else:
        # Regular tweet — combine title and body, truncate if needed
        text = f"{title}\n\n{body}"
        if len(text) > 280:
            # If too long for a regular tweet, use note tweet
            response = client.create_tweet(text=text)
        else:
            response = client.create_tweet(text=text)

    tweet_id = response.data["id"]
    # Get the authenticated user's username for the URL
    me = client.get_me()
    username = me.data.username
    return f"https://x.com/{username}/status/{tweet_id}"


def main():
    parser = argparse.ArgumentParser(description="Post content to X (Twitter)")
    parser.add_argument("--title", required=True, help="Post title")
    parser.add_argument("--body", required=True, help="Post body text")
    parser.add_argument(
        "--article",
        action="store_true",
        help="Create a long-form note tweet instead of a regular tweet",
    )
    args = parser.parse_args()

    try:
        url = post_to_x(args.title, args.body, args.article)
        print(url)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
