from app.config import settings

def reason(prompt: str) -> dict:
    if settings.llm_mode == "mock" or not settings.openai_api_key:
        return {"mode": "mock", "answer": "Use the deterministic parser and rules as the source of truth; no fabricated benchmark is available."}
    from openai import OpenAI
    response = OpenAI(api_key=settings.openai_api_key).chat.completions.create(model=settings.openai_model, messages=[{"role": "system", "content": "You explain verified SQL findings. Never invent execution metrics."}, {"role": "user", "content": prompt}], temperature=0)
    return {"mode": "openai-compatible", "answer": response.choices[0].message.content}
