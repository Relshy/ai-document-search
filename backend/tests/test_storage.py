from unittest.mock import MagicMock, patch

import pytest

from app.storage import search_chunks, store_chunks


def test_store_chunks_inserts_a_row_per_chunk() -> None:
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    with patch("app.storage.get_connection", return_value=mock_connection):
        store_chunks("notes.md", ["first chunk", "second chunk"], [[0.1], [0.2]])

    mock_cursor.executemany.assert_called_once_with(
        "INSERT INTO document_chunks (filename, content, embedding) VALUES (%s, %s, %s)",
        [
            ("notes.md", "first chunk", [0.1]),
            ("notes.md", "second chunk", [0.2]),
        ],
    )


def test_store_chunks_does_nothing_for_empty_input() -> None:
    with patch("app.storage.get_connection") as mock_get_connection:
        store_chunks("notes.md", [], [])

    mock_get_connection.assert_not_called()


def test_store_chunks_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        store_chunks("notes.md", ["chunk"], [])


def test_search_chunks_returns_closest_matches() -> None:
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
    mock_cursor.fetchall.return_value = [("notes.md", "first chunk", 0.1)]

    with patch("app.storage.get_connection", return_value=mock_connection):
        results = search_chunks([0.1, 0.2], limit=3)

    mock_cursor.execute.assert_called_once_with(
        """
            SELECT filename, content, embedding <-> %s AS distance
            FROM document_chunks
            ORDER BY distance
            LIMIT %s
            """,
        ([0.1, 0.2], 3),
    )
    assert results == [{"filename": "notes.md", "content": "first chunk", "distance": 0.1}]
