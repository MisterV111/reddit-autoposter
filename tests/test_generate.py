"""Tests for generate.py."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure we can import from src
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.generate import load_template, generate_article, TONE_MODIFIERS


def test_load_template():
    """Test that all pillar templates exist and load."""
    pillars = ["workflow", "review", "case_study", "tutorial", "business", "news"]
    for pillar in pillars:
        template = load_template(pillar)
        assert len(template) > 100, f"Template for {pillar} seems too short"
        assert "Article Rules" in template


def test_load_template_missing():
    """Test that missing template raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_template("nonexistent_pillar")


def test_tone_modifiers_exist():
    """Test that tone modifiers are defined."""
    assert len(TONE_MODIFIERS) >= 3


@patch("src.generate.anthropic.Anthropic")
def test_generate_article_basic(mock_anthropic_cls):
    """Test basic article generation with mocked API."""
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client

    fake_body = "This is a test article body. " * 100  # ~3000 chars
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=fake_body)]
    mock_client.messages.create.return_value = mock_message

    topic = {
        "title": "Test Topic",
        "pillar": "workflow",
        "keywords": ["test", "workflow"],
        "brief": "A test brief for article generation.",
    }
    config = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "temperature": 0.8,
        "min_length": 100,
        "max_length": 4000,
    }

    result = generate_article(topic, config)

    assert "title" in result
    assert "body" in result
    assert result["title"] == "Test Topic"
    assert len(result["body"]) > 0
    mock_client.messages.create.assert_called_once()


@patch("src.generate.anthropic.Anthropic")
def test_generate_article_retry_short(mock_anthropic_cls):
    """Test that short articles trigger a retry."""
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client

    short_body = "Too short."
    long_body = "This is now a longer article. " * 80

    mock_msg_short = MagicMock()
    mock_msg_short.content = [MagicMock(text=short_body)]
    mock_msg_long = MagicMock()
    mock_msg_long.content = [MagicMock(text=long_body)]

    mock_client.messages.create.side_effect = [mock_msg_short, mock_msg_long]

    topic = {
        "title": "Short Test",
        "pillar": "review",
        "keywords": ["test"],
        "brief": "Testing retry on short content.",
    }
    config = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "temperature": 0.8,
        "min_length": 1500,
        "max_length": 4000,
    }

    result = generate_article(topic, config)

    assert len(result["body"]) > 100
    assert mock_client.messages.create.call_count == 2
