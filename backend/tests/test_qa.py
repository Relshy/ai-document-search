from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.qa import answer_question, get_anthropic_client


def test_answer_question_returns_answer_with_citations() -> None:
    sources = [{"filename": "notes.md", "content": "The launch date is March 3rd.", "distance": 0.1}]
    text_block = SimpleNamespace(type="text", text="The launch date is March 3rd [1].")
    mock_client = MagicMock()
    mock_client.messages.create.return_value = SimpleNamespace(content=[text_block])

    with (
        patch("app.qa.embed_query", return_value=[0.1, 0.2]),
        patch("app.qa.search_chunks", return_value=sources),
        patch("app.qa.get_anthropic_client", return_value=mock_client),
    ):
        result = answer_question("When is the launch?")

    mock_client.messages.create.assert_called_once()
    assert result == {
        "answer": "The launch date is March 3rd [1].",
        "citations": [
            {"index": 1, "filename": "notes.md", "content": "The launch date is March 3rd."}
        ],
    }


def test_answer_question_handles_no_matching_sources() -> None:
    with (
        patch("app.qa.embed_query", return_value=[0.1, 0.2]),
        patch("app.qa.search_chunks", return_value=[]),
        patch("app.qa.get_anthropic_client") as mock_get_client,
    ):
        result = answer_question("When is the launch?")

    mock_get_client.assert_not_called()
    assert result == {
        "answer": "No relevant documents were found to answer this question.",
        "citations": [],
    }


def test_get_anthropic_client_requires_api_key(monkeypatch) -> None:
    get_anthropic_client.cache_clear()
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        get_anthropic_client()

    get_anthropic_client.cache_clear()
