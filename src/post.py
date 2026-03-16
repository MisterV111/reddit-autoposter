"""Reddit posting via PRAW. Works as both a library and CLI tool."""

import argparse
import os
import sys
import time

import praw
from dotenv import load_dotenv

load_dotenv()


def get_reddit_client() -> praw.Reddit:
    """Create and return an authenticated Reddit client."""
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent="reddit-autoposter/1.0 (by u/{})".format(
            os.environ["REDDIT_USERNAME"]
        ),
    )


def submit_post(
    title: str,
    body: str,
    subreddit_name: str,
    flair: str | None = None,
    max_retries: int = 3,
) -> str:
    """Submit a text post to a subreddit.

    Args:
        title: Post title
        body: Post body in markdown
        subreddit_name: Target subreddit (without r/)
        flair: Optional flair text
        max_retries: Number of retries on rate limit

    Returns:
        URL of the submitted post
    """
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)

    for attempt in range(max_retries):
        try:
            kwargs = {"title": title, "selftext": body}
            if flair:
                # Try to find matching flair
                try:
                    choices = list(subreddit.flair.link_templates)
                    match = next(
                        (f for f in choices if f["text"].lower() == flair.lower()),
                        None,
                    )
                    if match:
                        kwargs["flair_id"] = match["id"]
                        kwargs["flair_text"] = match["text"]
                except Exception:
                    pass  # Flair is optional, don't fail the post

            submission = subreddit.submit(**kwargs)
            return f"https://reddit.com{submission.permalink}"

        except praw.exceptions.RedditAPIException as e:
            for item in e.items:
                if item.error_type == "RATELIMIT":
                    # Parse wait time from message
                    msg = item.message.lower()
                    if "minute" in msg:
                        wait = 60
                    else:
                        wait = 10
                    print(f"Rate limited. Waiting {wait}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                    continue
            raise

    raise RuntimeError(f"Failed to submit post after {max_retries} attempts")


def main():
    parser = argparse.ArgumentParser(description="Post an article to Reddit")
    parser.add_argument("--title", required=True, help="Post title")
    parser.add_argument("--body", required=True, help="Post body (Reddit markdown)")
    parser.add_argument("--subreddit", required=True, help="Target subreddit (without r/)")
    parser.add_argument("--flair", default=None, help="Optional flair text")
    args = parser.parse_args()

    try:
        url = submit_post(args.title, args.body, args.subreddit, args.flair)
        print(url)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
