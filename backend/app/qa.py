import os
from functools import lru_cache

import anthropic

from app.embedding import embed_query
from app.storage import search_chunks

MODEL_NAME = "claude-sonnet-5"
MAX_ANSWER_TOKENS = 1024


@lru_cache(maxsize=1)
def get_anthropic_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")
    return anthropic.Anthropic(api_key=api_key)


def _build_prompt(query: str, sources: list[dict[str, object]]) -> str:
    numbered_sources = "\n\n".join(
        f"[{index}] ({source['filename']})\n{source['content']}"
        for index, source in enumerate(sources, start=1)
    )
    return (
        "Answer the question using only the numbered sources below. "
        "Cite sources inline using their bracketed number, e.g. [1]. "
        "If the sources do not contain the answer, say so.\n\n"
        f"Sources:\n{numbered_sources}\n\n"
        f"Question: {query}"
    )


def answer_question(query: str, limit: int = 5) -> dict[str, object]:
    query_embedding = embed_query(query)
    sources = search_chunks(query_embedding, limit=limit)

    if not sources:
        return {"answer": "No relevant documents were found to answer this question.", "citations": []}

    response = get_anthropic_client().messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_ANSWER_TOKENS,
        messages=[{"role": "user", "content": _build_prompt(query, sources)}],
    )
    answer = "".join(block.text for block in response.content if block.type == "text")

    citations = [
        {"filename": source["filename"], "content": source["content"]} for source in sources
    ]
    return {"answer": answer, "citations": citations}
