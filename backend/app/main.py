from fastapi import FastAPI

app = FastAPI(title="ai-document-search")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
