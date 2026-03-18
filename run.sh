#!/bin/bash
# ICG Content Engine — Claude Code entry point
# Runs via Claude Max Pro subscription (zero API costs)
export PATH="/opt/homebrew/bin:$PATH"
cd "$(dirname "$0")"

# --- Skill Resolver: Content Writing Craft ---
if [ -f "$(pwd)/skills/content-writing-craft/SKILL.md" ] && [ -s "$(pwd)/skills/content-writing-craft/SKILL.md" ]; then
  WRITING_SKILL="$(pwd)/skills/content-writing-craft/SKILL.md"
elif [ -f "$HOME/.claude/skills/content-writing-craft/SKILL.md" ] && [ -s "$HOME/.claude/skills/content-writing-craft/SKILL.md" ]; then
  WRITING_SKILL="$HOME/.claude/skills/content-writing-craft/SKILL.md"
else
  WRITING_SKILL=""
fi

# --- Skill Resolver: Stop Slop (AI tell removal) ---
if [ -f "$(pwd)/skills/stop-slop/SKILL.md" ] && [ -s "$(pwd)/skills/stop-slop/SKILL.md" ]; then
  STOP_SLOP_SKILL="$(pwd)/skills/stop-slop/SKILL.md"
  STOP_SLOP_REFS="$(pwd)/skills/stop-slop/references/"
elif [ -f "$HOME/.claude/skills/stop-slop/SKILL.md" ] && [ -s "$HOME/.claude/skills/stop-slop/SKILL.md" ]; then
  STOP_SLOP_SKILL="$HOME/.claude/skills/stop-slop/SKILL.md"
  STOP_SLOP_REFS="$HOME/.claude/skills/stop-slop/references/"
else
  STOP_SLOP_SKILL=""
  STOP_SLOP_REFS=""
fi

# --- Build skill instructions ---
WRITING_INSTRUCTION=""
[ -n "$WRITING_SKILL" ] && WRITING_INSTRUCTION="Read $WRITING_SKILL and apply its craft principles when writing."

SLOP_INSTRUCTION=""
[ -n "$STOP_SLOP_SKILL" ] && SLOP_INSTRUCTION="After writing each article variant, run a stop-slop pass: read $STOP_SLOP_SKILL and its reference files at ${STOP_SLOP_REFS} (phrases.md, structures.md, examples.md), then score the article against the rubric (Directness, Rhythm, Trust, Authenticity, Density). If score is below 35/50, rewrite. This is mandatory — no article posts without passing the stop-slop check."

# --- Run the content engine ---
claude --print -p "Read CLAUDE.md and PERSONA.md completely first. $WRITING_INSTRUCTION $SLOP_INSTRUCTION Then execute the full autoresearch pipeline as described in CLAUDE.md: research trending topics, generate 3 article variants, score and select the winner, AI-proof it, run the stop-slop pass, create platform adaptations for Reddit, LinkedIn, and X, then post using the scripts in src/. See CLAUDE.md for full instructions."
