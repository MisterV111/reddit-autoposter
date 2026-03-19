"""LinkedIn posting via OAuth 2.0 REST API. Works as both a library and CLI tool."""

import argparse
import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()


def post_to_linkedin(title: str, body: str, article: bool = False) -> str:
    """Post content to LinkedIn personal profile.

    Args:
        title: Post title (used as prefix for regular posts, article title for articles)
        body: Post body text
        article: If True, creates an article; otherwise creates a regular post

    Returns:
        URL of the posted content
    """
    access_token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    person_id = os.environ["LINKEDIN_PERSON_ID"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202402",
    }

    if article:
        # LinkedIn articles via UGC API. Note: true LinkedIn Articles (the blog
        # format with SEO indexing) require manual publishing via the web UI.
        # This endpoint creates a share with ARTICLE media category, which is
        # the closest API equivalent. For full articles, consider posting via
        # the web UI and using this as a fallback.
        post_data = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": body},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": "",
                            "title": {"text": title},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }
        endpoint = "https://api.linkedin.com/v2/ugcPosts"
    else:
        # Regular post using /v2/posts (Community Management API)
        text = f"{title}\n\n{body}" if title else body
        post_data = {
            "author": f"urn:li:person:{person_id}",
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
        }
        endpoint = "https://api.linkedin.com/rest/posts"

    response = requests.post(endpoint, headers=headers, json=post_data, timeout=30)

    if response.status_code in (200, 201):
        # Extract post ID from response header or body
        post_id = response.headers.get("x-restli-id", "")
        if not post_id and response.text:
            try:
                resp_data = response.json()
                post_id = resp_data.get("id", "")
            except (json.JSONDecodeError, KeyError):
                pass
        if post_id:
            # Clean URN format for URL
            clean_id = post_id.replace("urn:li:share:", "").replace("urn:li:ugcPost:", "")
            return f"https://www.linkedin.com/feed/update/urn:li:share:{clean_id}/"
        return f"https://www.linkedin.com/in/{person_id}/recent-activity/"
    else:
        raise RuntimeError(
            f"LinkedIn API error {response.status_code}: {response.text}"
        )


def main():
    parser = argparse.ArgumentParser(description="Post content to LinkedIn")
    parser.add_argument("--title", required=True, help="Post title")
    parser.add_argument("--body", required=True, help="Post body text")
    parser.add_argument(
        "--article",
        action="store_true",
        help="Create a LinkedIn article instead of a regular post",
    )
    args = parser.parse_args()

    try:
        url = post_to_linkedin(args.title, args.body, args.article)
        print(url)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
