#!/bin/bash
# Content Engine — Claude Code entry point (Reddit + LinkedIn + X)
# Runs via Claude Max Pro subscription (zero API costs)
export PATH="/opt/homebrew/bin:$PATH"
cd "$(dirname "$0")"

claude --print -p "You are the AI Production Content Engine. Read CLAUDE.md and PERSONA.md for your full instructions and editorial voice. Follow every step: research trending topics, verify tool versions, generate 3 article variants, score them (8+ to post), AI-proof the winner, create platform-specific versions for Reddit/LinkedIn/X, then post using src/post_reddit.py, src/post_linkedin.py, and src/post_x.py. Log everything to data/experiment-log.jsonl and data/post-history.jsonl. Update content-queue.jsonl when done."
