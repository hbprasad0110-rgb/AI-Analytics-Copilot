import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "copilot_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )

def run_sql(sql: str, limit: int = 200):
    # Safety: force LIMIT if not present
    sql_clean = sql.strip().rstrip(";")
    if "limit" not in sql_clean.lower():
        sql_clean += f" LIMIT {limit}"

    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql_clean)
            rows = cur.fetchall()
            return rows
