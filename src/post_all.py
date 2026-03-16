"""Multi-platform posting orchestrator. Posts to Reddit, LinkedIn, and X."""

import argparse
import json
import sys
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(
        description="Post content to all platforms (Reddit, LinkedIn, X)"
    )
    parser.add_argument("--title", required=True, help="Post title")
    parser.add_argument("--reddit-body", required=True, help="Reddit version of the post")
    parser.add_argument("--linkedin-body", required=True, help="LinkedIn version of the post")
    parser.add_argument("--x-body", required=True, help="X version of the post")
    parser.add_argument("--subreddit", default="AIProductionHouse", help="Target subreddit")
    parser.add_argument("--flair", default=None, help="Reddit flair text")
    args = parser.parse_args()

    results = {}
    failures = {}

    # Post to Reddit
    try:
        from post_reddit import submit_post

        url = submit_post(args.title, args.reddit_body, args.subreddit, args.flair)
        results["reddit"] = url
        print(f"Reddit: {url}")
    except Exception as e:
        failures["reddit"] = str(e)
        print(f"Reddit FAILED: {e}", file=sys.stderr)

    # Post to LinkedIn
    try:
        from post_linkedin import post_to_linkedin

        url = post_to_linkedin(args.title, args.linkedin_body)
        results["linkedin"] = url
        print(f"LinkedIn: {url}")
    except Exception as e:
        failures["linkedin"] = str(e)
        print(f"LinkedIn FAILED: {e}", file=sys.stderr)

    # Post to X
    try:
        from post_x import post_to_x

        url = post_to_x(args.title, args.x_body, article=True)
        results["x"] = url
        print(f"X: {url}")
    except Exception as e:
        failures["x"] = str(e)
        print(f"X FAILED: {e}", file=sys.stderr)

    # Print summary
    print(f"\n--- Summary ---")
    print(f"Posted: {', '.join(results.keys()) if results else 'none'}")
    if failures:
        print(f"Failed: {', '.join(failures.keys())}")

    # Output JSON summary for programmatic use
    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": args.title,
        "posted": results,
        "failed": failures,
    }
    print(f"\n{json.dumps(summary)}")

    # Exit 0 if at least one platform succeeded, 1 if all failed
    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
