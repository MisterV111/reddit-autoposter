"""Article generation using Claude API.

This module is OPTIONAL — the primary workflow uses Claude Code (run.sh)
which has zero API costs via the Max Pro subscription.

Keep this for batch pre-generation if you want to use the API directly.
Requires: pip install anthropic
"""

import os
import random
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

# Tone variations to keep content feeling human
TONE_MODIFIERS = [
    "Write in a direct, no-BS tone. Like you're explaining to a colleague over coffee.",
    "Write with analytical precision. Back up claims with specifics. Slightly formal.",
    "Write casually but knowledgeably — like a senior creator sharing tips on a forum.",
    "Write with enthusiasm about what works, skepticism about what doesn't. Be opinionated.",
    "Write in a practical, get-things-done tone. Minimal fluff, maximum actionable advice.",
]


def load_template(pillar: str) -> str:
    """Load the prompt template for a given content pillar."""
    template_path = TEMPLATES_DIR / f"{pillar}.md"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text()


def generate_article(topic: dict, config: dict) -> dict:
    """Generate a Reddit article from a topic dict and config.

    Requires the 'anthropic' package to be installed.

    Args:
        topic: Dict with keys: title, pillar, keywords, brief
        config: Generation config with model, max_tokens, temperature

    Returns:
        Dict with 'title' and 'body' keys
    """
    try:
        import anthropic
    except ImportError:
        raise ImportError(
            "The 'anthropic' package is required for API-based generation. "
            "Install it with: pip install anthropic\n"
            "Or use run.sh for zero-cost generation via Claude Code."
        )

    client = anthropic.Anthropic()

    template = load_template(topic["pillar"])
    tone = random.choice(TONE_MODIFIERS)

    prompt = f"""{template}

---

**Topic:** {topic['title']}
**Keywords:** {', '.join(topic['keywords'])}
**Brief:** {topic['brief']}

**Tone instruction:** {tone}

Write the article now. Output ONLY the article body in Reddit markdown format.
Do not include the title — it will be used as the Reddit post title separately.
Target length: 2000-4000 characters."""

    message = client.messages.create(
        model=config.get("model", "claude-sonnet-4-20250514"),
        max_tokens=config.get("max_tokens", 4096),
        temperature=config.get("temperature", 0.8),
        messages=[{"role": "user", "content": prompt}],
    )

    body = message.content[0].text.strip()

    # Basic quality checks
    min_len = config.get("min_length", 1500)
    max_len = config.get("max_length", 4000)
    if len(body) < min_len:
        # Retry once with explicit length instruction
        message = client.messages.create(
            model=config.get("model", "claude-sonnet-4-20250514"),
            max_tokens=config.get("max_tokens", 4096),
            temperature=config.get("temperature", 0.8),
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": body},
                {
                    "role": "user",
                    "content": f"This is too short ({len(body)} chars). Expand it to at least {min_len} characters with more detail and examples. Output the full revised article.",
                },
            ],
        )
        body = message.content[0].text.strip()

    # Truncate if too long
    if len(body) > max_len:
        # Find a clean break point
        cut = body[:max_len].rfind("\n\n")
        if cut > max_len * 0.7:
            body = body[:cut]
        else:
            body = body[:max_len]

    return {"title": topic["title"], "body": body}
