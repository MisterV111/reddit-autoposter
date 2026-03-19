# AI Production Content Engine

Multi-platform content pipeline for AI production communities. Claude Code researches trending topics, writes articles, and posts to **Reddit**, **LinkedIn**, and **X** — zero API costs through your Claude Max Pro subscription.

## Architecture

```
LaunchAgent/cron → run.sh → Claude Code (--print mode)
                                 ↓
                    1. Research: Brave Search for trending Reddit topics
                    2. Verify: Check current tool versions/pricing
                    3. Generate: 3 article variants with different angles
                    4. Score: Rubric-based evaluation (8+/10 to post)
                    5. AI-Proof: Sentence variation, first-person, opinions
                    6. Adapt: 5 platform formats (Reddit post, LinkedIn post/article, X post/article)
                    7. Post: src/post_reddit.py, post_linkedin.py, post_x.py
                    8. Log: experiment-log.jsonl + post-history.jsonl
```

This is an **autoresearch pattern** — Claude Code researches before writing, verifies facts, generates multiple variants, scores them, and only posts if quality threshold is met.

## Platforms (5 Output Formats)

| Platform | Format | Module | Voice |
|----------|--------|--------|-------|
| Reddit | Post | `src/post_reddit.py` | Casual practitioner, Reddit markdown, 2,000-3,500 chars |
| LinkedIn | Post | `src/post_linkedin.py` | Professional authority, 1,200-1,500 chars, scroll-stopping |
| LinkedIn | Article | `src/post_linkedin.py --article` | Blog-style, SEO-indexed, 2,500-4,000+ chars |
| X | Post | `src/post_x.py` | Punchy hot takes, 280-1,800 chars, feed engagement |
| X | Article | `src/post_x.py --article` | Long-form thought leadership, 2,500-4,000+ chars |

## Content Pillars

| Pillar | Focus |
|--------|-------|
| **Workflow** | Step-by-step AI production processes |
| **Review** | Tool comparisons with honest verdicts |
| **Business** | Pricing, proposals, client management |
| **Case Study** | Production breakdowns with timelines/costs |
| **News** | Industry developments and analysis |
| **Tutorial** | Detailed how-to guides |

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Fill in credentials for each platform you want to post to:

**Reddit** — Create a "script" app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)

**LinkedIn** — Get an OAuth 2.0 access token via [LinkedIn Developer Portal](https://developer.linkedin.com/). You need the `w_member_social` scope. Find your Person ID via the `/v2/userinfo` endpoint.

**X (Twitter)** — Create a project at [developer.twitter.com](https://developer.twitter.com/). Enable OAuth 1.0a with read+write permissions. Generate access tokens in your app settings.

### 3. Claude Code

Install and authenticate Claude Code (`claude` CLI in PATH). No Anthropic API key needed — runs through Max Pro subscription.

### 4. Seed topics

```bash
python src/seed_topics.py
```

Generates 50+ topics to `content-queue.jsonl`.

## Usage

### Run the full pipeline (research → write → post)

```bash
./run.sh
```

Claude Code reads `CLAUDE.md` instructions, researches, writes, scores, and posts.

### Post manually to individual platforms

```bash
# Reddit
python3 src/post_reddit.py --title "Title" --body "Body" --subreddit AIProductionHouse

# LinkedIn
python3 src/post_linkedin.py --title "Title" --body "Body"

# X
python3 src/post_x.py --title "Title" --body "Body"

# All platforms
python3 src/post_all.py --title "Title" --reddit-body "..." --linkedin-body "..." --x-body "..." --subreddit AIProductionHouse
```

### Legacy: API-based generation

```bash
pip install anthropic
python src/scheduler.py --dry-run
```

Requires `ANTHROPIC_API_KEY` in `.env`.

## Review Workflow

The engine generates 3 variants, picks a winner, then creates 5 platform-specific formats. It does NOT auto-post. Instead, it saves all formats and notifies Juan for human review.

### How it works

1. Engine generates 3 variants, scores them, picks a winner
2. Creates 5 platform formats from the winner: Reddit post, LinkedIn post, LinkedIn article, X post, X article
3. Saves to `data/review/[run-id]/` with `metadata.json`
4. Sends notification with per-platform format options and char counts
5. Juan picks format per platform (e.g., "reddit, linkedin article, x post")

### Approve and post with per-platform format selection

```bash
# Pick format per platform
python3 src/post_choice.py --run-id 2026-03-18-143022 --reddit post --linkedin article --x post

# Shortcuts
python3 src/post_choice.py --run-id 2026-03-18-143022 --all articles
python3 src/post_choice.py --run-id 2026-03-18-143022 --all posts
```

Each platform flag accepts: `post`, `article`, `skip`, or `both`. Logs choices to `data/preference-log.jsonl`.

### Notification CLI (standalone)

```bash
python3 src/notify.py --topic "Topic Name" \
  --variant-a "Practitioner walkthrough 8.5" \
  --variant-b "Comparison piece 7.9" \
  --variant-c "Hot take 8.2" \
  --winner A --slop-score 8.5 \
  --reddit-post-chars 2800 \
  --linkedin-post-chars 1350 --linkedin-article-chars 3200 \
  --x-post-chars 1100 --x-article-chars 3400
```

Falls back to stdout if the agent gateway is unavailable.

## Deploy (macOS LaunchAgent)

Create `~/Library/LaunchAgents/com.contentengine.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.contentengine</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/juancarlosvalencia/Documents/AI - Programming Projects/reddit-autoposter/run.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>21600</integer>
    <key>StandardOutPath</key>
    <string>/tmp/content-engine.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/content-engine.err</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.contentengine.plist
```

## Project Structure

```
reddit-autoposter/
├── run.sh                   # Entry point — launches Claude Code
├── CLAUDE.md                # Autoresearch instructions (THE brain)
├── config.json              # Subreddit, schedule, generation settings
├── content-queue.jsonl      # Topic queue (seeded by seed_topics.py)
├── src/
│   ├── post_reddit.py       # Reddit posting via PRAW
│   ├── post_linkedin.py     # LinkedIn posting via OAuth 2.0
│   ├── post_x.py            # X posting via Tweepy
│   ├── post_all.py          # Multi-platform orchestrator
│   ├── notify.py            # Telegram review notification
│   ├── post_choice.py       # Post Juan's chosen variant
│   ├── generate.py          # Optional: API-based generation
│   ├── scheduler.py         # Optional: API-based orchestrator
│   └── seed_topics.py       # Topic queue generator
├── data/
│   ├── experiment-log.jsonl  # Full run logs (research, scores, variants)
│   ├── post-history.jsonl    # Individual post logs
│   ├── evolution-log.jsonl   # Weekly self-improvement changes
│   ├── preference-log.jsonl  # Juan's choices vs system picks
│   └── review/               # Saved variants pending human review
├── templates/               # Pillar-specific prompt templates
├── samples/                 # Sample articles for quality reference
└── tests/
    └── test_generate.py
```

## Cost

**$0 extra.** Claude Code runs through Max Pro subscription. Reddit/LinkedIn/X APIs are free for personal use.
