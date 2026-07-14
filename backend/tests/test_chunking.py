import pytest

from app.chunking import chunk_text


def test_chunk_text_returns_empty_list_for_blank_text() -> None:
    assert chunk_text("   ") == []


def test_chunk_text_returns_single_chunk_when_text_fits() -> None:
    text = "one two three"

    chunks = chunk_text(text, chunk_size=100, chunk_overlap=10)

    assert chunks == ["one two three"]


def test_chunk_text_splits_long_text_into_multiple_chunks() -> None:
    text = " ".join(f"word{i}" for i in range(50))

    chunks = chunk_text(text, chunk_size=50, chunk_overlap=10)

    assert len(chunks) > 1
    assert all(len(chunk) <= 50 for chunk in chunks)


def test_chunk_text_overlaps_consecutive_chunks() -> None:
    text = " ".join(f"word{i}" for i in range(50))

    chunks = chunk_text(text, chunk_size=50, chunk_overlap=10)

    first_words = chunks[0].split()
    second_words = chunks[1].split()
    assert first_words[-1] in second_words


def test_chunk_text_preserves_all_words_across_chunks() -> None:
    words = [f"word{i}" for i in range(50)]
    text = " ".join(words)

    chunks = chunk_text(text, chunk_size=50, chunk_overlap=10)

    covered_words = set()
    for chunk in chunks:
        covered_words.update(chunk.split())
    assert covered_words == set(words)


def test_chunk_text_rejects_non_positive_chunk_size() -> None:
    with pytest.raises(ValueError):
        chunk_text("some text", chunk_size=0)


def test_chunk_text_rejects_overlap_not_smaller_than_chunk_size() -> None:
    with pytest.raises(ValueError):
        chunk_text("some text", chunk_size=10, chunk_overlap=10)
