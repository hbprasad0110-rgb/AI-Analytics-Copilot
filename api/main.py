import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from llm_ollama import generate_sql
from db import run_sql

load_dotenv()

app = FastAPI()

class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question is empty")

    sql = generate_sql(q)

    # Safety checks
    if not sql.lower().startswith("select"):
        raise HTTPException(status_code=400, detail=f"Unsafe SQL generated: {sql[:80]}")

    rows = run_sql(sql)
    return {"question": q, "sql": sql, "data": rows}
