import os
import requests
from schema import SCHEMA_TEXT

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")

SYSTEM_PROMPT = f"""
You are an expert data analyst. Convert user questions into SAFE PostgreSQL SQL queries.

Rules:
- Output ONLY SQL (no markdown, no explanations).
- Use only SELECT queries.
- Use only tables/columns from the schema.
- Use GROUP BY for aggregates.
- For revenue: SUM(quantity * price)
- Always include LIMIT (top-N uses LIMIT N, otherwise LIMIT 200)

Schema:
{SCHEMA_TEXT}

Example:
Question: orders by status
SQL:
SELECT status, COUNT(*) AS cnt
FROM orders
GROUP BY status
ORDER BY cnt DESC
LIMIT 20;

Question: top 5 products by revenue
SQL:
SELECT product, SUM(quantity * price) AS revenue
FROM order_items
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;
""".strip()

def _clean_sql(text: str) -> str:
    sql = (text or "").strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    # If model returns extra text, keep from first SELECT
    lower = sql.lower()
    idx = lower.find("select")
    if idx != -1:
        sql = sql[idx:]
    return sql.strip().rstrip(";") + ";"

def generate_sql(question: str) -> str:
    # 1) Try /api/chat (newer)
    chat_payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{question}\nReturn ONLY SQL."}
        ],
        "stream": False
    }
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=chat_payload, timeout=120)
        if r.status_code != 404:
            r.raise_for_status()
            data = r.json()
            return _clean_sql(data["message"]["content"])
    except requests.RequestException:
        pass

    # 2) Fallback to /api/generate (older)
    gen_payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser question: {question}\nSQL:",
        "stream": False
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=gen_payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return _clean_sql(data.get("response", ""))
