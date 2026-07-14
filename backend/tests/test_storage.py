from unittest.mock import MagicMock, patch

import pytest

from app.storage import store_chunks


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
