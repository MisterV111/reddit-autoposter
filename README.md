# Reddit Autoposter — AI Production Content Engine

Automated Reddit content pipeline that generates AI production articles via Claude API and posts them to r/AIProductionHouse using PRAW.

## What It Does

1. Picks the next unposted topic from a seeded content queue (50+ topics across 6 pillars)
2. Generates a Reddit-formatted article using Claude with pillar-specific prompt templates
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

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

You need:
- **Anthropic API key** — from [console.anthropic.com](https://console.anthropic.com)
- **Reddit API credentials** — create an app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) (select "script" type)

### 3. Edit config.json

Set your target subreddit and posting preferences. Posting is disabled by default.

### 4. Seed topics

```bash
python src/seed_topics.py
```

This generates 50+ topics to `content-queue.jsonl`.

## Usage

### Dry run (generate but don't post)

```bash
python src/scheduler.py --dry-run
```

### Dry run with saved output

```bash
python src/scheduler.py --dry-run --save-to samples/test.md
```

### Live posting

1. Set `posting.enabled` to `true` in `config.json`
2. Run:

```bash
python src/scheduler.py
```

### Environment variable dry run

```bash
DRY_RUN=true python src/scheduler.py
```

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
        <string>/opt/homebrew/bin/python3</string>
        <string>/path/to/reddit-autoposter/src/scheduler.py</string>
    </array>
    <key>StartInterval</key>
    <integer>21600</integer>
    <key>WorkingDirectory</key>
    <string>/path/to/reddit-autoposter</string>
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
0 */6 * * * cd /path/to/reddit-autoposter && /opt/homebrew/bin/python3 src/scheduler.py >> /tmp/reddit-autoposter.log 2>&1
```

## Project Structure

```
reddit-autoposter/
├── config.json              # Subreddit, schedule, generation settings
├── content-queue.jsonl      # Topic queue (seeded by seed_topics.py)
├── post-history.jsonl       # Posting log
├── src/
│   ├── generate.py          # Claude API article generation
│   ├── post.py              # PRAW Reddit posting
│   ├── scheduler.py         # Main entry point
│   └── seed_topics.py       # Topic queue generator
├── templates/               # Pillar-specific prompt templates
│   ├── workflow.md
│   ├── review.md
│   ├── case_study.md
│   ├── tutorial.md
│   ├── business.md
│   └── news.md
├── samples/                 # Generated sample articles
└── tests/
    └── test_generate.py
```

## Regenerating Topics

To add fresh topics, edit `src/seed_topics.py` and run it again. This overwrites the queue — any unposted topics will be replaced. Back up `content-queue.jsonl` first if needed.
