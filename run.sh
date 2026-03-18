#!/bin/bash
# Reddit Autoposter — Claude Code entry point
# Runs via Claude Max Pro subscription (zero API costs)
export PATH="/opt/homebrew/bin:$PATH"
cd "$(dirname "$0")"

# Resolve writing craft skill (local takes priority over global)
if [ -f "$(pwd)/skills/content-writing-craft/SKILL.md" ] && [ -s "$(pwd)/skills/content-writing-craft/SKILL.md" ]; then
  WRITING_SKILL_PATH="$(pwd)/skills/content-writing-craft/SKILL.md"
  WRITING_SKILL_INSTRUCTION="Also read $WRITING_SKILL_PATH and apply its craft principles to the article generation."
elif [ -f "$HOME/.claude/skills/content-writing-craft/SKILL.md" ] && [ -s "$HOME/.claude/skills/content-writing-craft/SKILL.md" ]; then
  WRITING_SKILL_PATH="$HOME/.claude/skills/content-writing-craft/SKILL.md"
  WRITING_SKILL_INSTRUCTION="Also read $WRITING_SKILL_PATH and apply its craft principles to the article generation."
else
  WRITING_SKILL_INSTRUCTION=""
fi

# Run the content engine
claude --print -p "Read CLAUDE.md and PERSONA.md completely first. $WRITING_SKILL_INSTRUCTION Then execute the full autoresearch pipeline as described in CLAUDE.md: research trending topics, generate 3 article variants, score and select the winner, AI-proof it, create platform adaptations for Reddit, LinkedIn, and X, then post using the scripts in src/. See CLAUDE.md for full instructions."
