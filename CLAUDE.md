# Build guidance for ai-document-search

A self-hosted service that ingests documents, embeds them for semantic retrieval, and answers questions with cited sources.

## Pinned tech stack

These are chosen so sessions build one coherent system rather than re-deciding each time. Change one only with a clear reason recorded in the commit message.

- Backend: Python + FastAPI
- Vector store: PostgreSQL with pgvector
- Embeddings: sentence-transformers
- OCR: Tesseract
- Question answering: Claude API
- Frontend: React + TypeScript
- Deployment: Docker Compose

## Build order

Work foundations before features, and features before extras. Within a session, advance one task or one coherent slice end to end.

1. Foundation: scaffold, Docker Compose with Postgres and pgvector, health endpoint, app shell, and tests.
2. Upload and parsing for PDF and Markdown.
3. Chunking, embedding, and vector storage.
4. Semantic search over the store.
5. OCR for scanned documents.
6. Question answering with highlighted citations.

## How to run and test

- Use the stack above. Provide a Docker Compose that starts the dependencies.
- Keep the application runnable for whatever is implemented so far.
- Every package must have a test command that runs its tests.

## Definition of done for a session

- Advance one README task, or a coherent slice of one, and tick it when done.
- Add or update tests for the behaviour you implement.
- Keep the project building and its tests passing.
- Update documentation only when your change makes it inaccurate.
- Make a single cohesive local commit with a clear message. Do not push.
- If a task cannot be advanced safely, explain why and make no changes.

## Coding standards

You are an experienced software engineer writing production-quality code.

General principles
- Prioritise readability over cleverness.
- Keep implementations simple and maintainable.
- Write code another engineer can understand quickly.
- Prefer composition over unnecessary abstraction.
- Avoid premature optimization.
- Every file should have a clear responsibility.

Code quality
- Never leave dead code, commented-out code, or placeholder implementations unless
  explicitly requested.
- Remove unused imports, variables, functions, and files.
- Avoid duplicate logic; refactor into reusable functions only when it improves clarity.
- Keep functions focused on a single responsibility.
- Avoid deeply nested conditionals; prefer early returns.

Project structure
- Keep a logical folder structure and consistent naming.
- Separate business logic from UI, and configuration from implementation.
- Keep modules cohesive; avoid "misc", "utils", or "helpers" dumping grounds.

Comments
- Explain why, not what, and only when it adds value.
- Prefer self-documenting code. Use sentence case.
- No all-caps comments and no decorative comment banners.
- Remove outdated comments immediately.

Naming
- Use descriptive names; avoid abbreviations unless industry standard.
- Boolean names should read naturally; function names should describe an action.
- Avoid generic names like data, temp, obj, item, value, manager, helper, or util
  unless appropriate.

Formatting
- Keep files consistently formatted with reasonable line lengths.
- Avoid excessive whitespace; keep related code grouped.

Error handling
- Fail gracefully and return useful error messages.
- Never silently swallow exceptions; avoid catch-all handlers unless justified.
- Validate inputs where appropriate.

Dependencies
- Do not introduce new dependencies without a clear benefit.
- Prefer standard library and existing project features first.
- Remove unused packages.

Logging
- Log meaningful events only; avoid excessive debug logging.
- Never log secrets or sensitive information.

Testing
- Write tests for new behaviour and update tests when behaviour changes.
- Avoid brittle tests; remove obsolete tests.

Git
- Make cohesive, focused commits for one logical change.
- Avoid unrelated modifications. Update documentation when behaviour changes.

Documentation
- Keep READMEs accurate and document public APIs when appropriate.
- Remove outdated documentation.

Style
- Never use emojis in code, logs, comments, commit messages, or documentation.
- Use simple symbols when needed. Maintain a professional tone and keep output concise.
- Do not generate unnecessary boilerplate.

AI-specific
- Do not invent architecture that is not needed, and do not over-engineer.
- Do not create unnecessary wrapper classes or files.
- Do not leave TODOs unless explicitly requested, and do not assume future requirements.
- Follow existing patterns when they are used consistently.
- Before finishing, review the whole change, remove redundant code, simplify logic,
  and ensure the result is production-ready.
