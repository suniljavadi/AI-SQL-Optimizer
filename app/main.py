from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI SQL Query Optimizer", version="1.0.0")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "llm_mode": "mock", "database": "synthetic"}
