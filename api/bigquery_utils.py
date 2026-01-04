from google.cloud import bigquery

def run_query(sql: str):
    client = bigquery.Client()
    job = client.query(sql)
    rows = list(job.result())

    columns = [field.name for field in job.schema]
    data = [dict(zip(columns, [r[c] for c in columns])) for r in rows]

    return columns, data
