# Reddit Autoposter — AI Production Content Engine

Automated Reddit content pipeline for r/AIProductionHouse. Claude Code writes the articles and posts them via PRAW — **zero API costs** through your Claude Max Pro subscription.

## Architecture

```
LaunchAgent/cron → run.sh → Claude Code (--print mode)
                                 ↓
                    Reads topic from content-queue.jsonl
                    Reads pillar template from templates/
                    Writes the article
                    Calls python3 src/post.py → Reddit
                    Updates queue + history
```

Claude Code **is** the writer. No API key needed — everything runs through your Max Pro subscription.

## What It Does

1. Picks the next unposted topic from a seeded content queue (50+ topics across 6 pillars)
2. Claude Code reads the pillar-specific template and writes a Reddit-formatted article
3. Posts to the target subreddit via PRAW
4. Logs the result and marks the topic as posted
5. Designed to run on a schedule (cron/LaunchAgent)

## Content Pillars

| Pillar | Description |
|--------|-------------|
| **Workflow** | Step-by-step AI production processes |
| **Review** | Tool comparisons with honest verdicts |
| **Business** | Pricing, proposals, client management |
| **Case Study** | Production breakdowns with timelines and costs |
| **News** | Industry developments and analysis |
| **Tutorial** | Detailed how-to guides for specific tasks |

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your Reddit credentials:

```bash
cp .env.example .env
```

You need:
- **Reddit API credentials** — create an app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) (select "script" type)
- **Claude Code** installed and authenticated (`claude` CLI available in PATH)

No Anthropic API key needed.

### 3. Edit config.json

Set your target subreddit and posting preferences. Posting is disabled by default.

### 4. Seed topics

```bash
python src/seed_topics.py
```

This generates 50+ topics to `content-queue.jsonl`.

## Usage

### Run once (Claude Code writes + posts)

```bash
./run.sh
```

This starts Claude Code in `--print` mode. It reads the next topic, writes the article, and posts it.

### Post manually (CLI)

```bash
python3 src/post.py --title "Your Title" --body "Your article body" --subreddit AIProductionHouse
```

### Legacy: API-based generation (optional)

If you want to use the Anthropic API directly instead of Claude Code:

```bash
pip install anthropic
python src/scheduler.py --dry-run
```

This requires an `ANTHROPIC_API_KEY` in your `.env`.

## Deploy as LaunchAgent (macOS)

Create `~/Library/LaunchAgents/com.autoposter.reddit.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.autoposter.reddit</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/juancarlosvalencia/Documents/AI - Programming Projects/reddit-autoposter/run.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>21600</integer>
    <key>StandardOutPath</key>
    <string>/tmp/reddit-autoposter.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/reddit-autoposter.err</string>
</dict>
</plist>
```

Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.autoposter.reddit.plist
```

## Deploy with cron

```bash
# Post every 6 hours
0 */6 * * * /bin/bash "/Users/juancarlosvalencia/Documents/AI - Programming Projects/reddit-autoposter/run.sh" >> /tmp/reddit-autoposter.log 2>&1
```

## Project Structure

```
reddit-autoposter/
├── run.sh                   # Entry point — launches Claude Code
├── CLAUDE.md                # Instructions for Claude Code
├── config.json              # Subreddit, schedule, generation settings
├── content-queue.jsonl      # Topic queue (seeded by seed_topics.py)
├── post-history.jsonl       # Posting log
├── src/
│   ├── post.py              # CLI + library — posts to Reddit via PRAW
│   ├── generate.py          # Optional: API-based generation (requires anthropic)
│   ├── scheduler.py         # Optional: API-based orchestrator
│   └── seed_topics.py       # Topic queue generator
├── templates/               # Pillar-specific prompt templates
│   ├── workflow.md
│   ├── review.md
│   ├── case_study.md
│   ├── tutorial.md
│   ├── business.md
│   └── news.md
├── samples/                 # Sample articles for quality reference
└── tests/
    └── test_generate.py
```

## Regenerating Topics

To add fresh topics, edit `src/seed_topics.py` and run it again. This overwrites the queue — any unposted topics will be replaced. Back up `content-queue.jsonl` first if needed.

## Cost

**$0 extra.** Claude Code runs through your Max Pro subscription. Reddit API is free for script-type apps.
