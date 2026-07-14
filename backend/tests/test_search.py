from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_returns_matching_chunks() -> None:
    with (
        patch("app.main.embed_query", return_value=[0.1, 0.2]) as mock_embed_query,
        patch(
            "app.main.search_chunks",
            return_value=[{"filename": "notes.md", "content": "first chunk", "distance": 0.1}],
        ) as mock_search_chunks,
    ):
        response = client.get("/search", params={"query": "notes about the project"})

    mock_embed_query.assert_called_once_with("notes about the project")
    mock_search_chunks.assert_called_once_with([0.1, 0.2], limit=5)

    assert response.status_code == 200
    assert response.json() == {
        "query": "notes about the project",
        "results": [{"filename": "notes.md", "content": "first chunk", "distance": 0.1}],
    }


def test_search_rejects_empty_query() -> None:
    response = client.get("/search", params={"query": "   "})

    assert response.status_code == 422
    assert response.json()["detail"] == "query must not be empty"


def test_ask_returns_answer_with_citations() -> None:
    with patch(
        "app.main.answer_question",
        return_value={
            "answer": "The launch date is March 3rd [1].",
            "citations": [{"filename": "notes.md", "content": "The launch date is March 3rd."}],
        },
    ) as mock_answer_question:
        response = client.get("/ask", params={"query": "When is the launch?"})

    mock_answer_question.assert_called_once_with("When is the launch?", limit=5)

    assert response.status_code == 200
    assert response.json() == {
        "query": "When is the launch?",
        "answer": "The launch date is March 3rd [1].",
        "citations": [{"filename": "notes.md", "content": "The launch date is March 3rd."}],
    }


def test_ask_rejects_empty_query() -> None:
    response = client.get("/ask", params={"query": "   "})

    assert response.status_code == 422
    assert response.json()["detail"] == "query must not be empty"
