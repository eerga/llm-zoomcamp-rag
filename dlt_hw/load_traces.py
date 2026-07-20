from dotenv import load_dotenv
load_dotenv()

import os
import dlt
import requests

LOGFIRE_READ_TOKEN = os.environ["LOGFIRE_READ_TOKEN"]
LOGFIRE_BASE_URL = "https://logfire-us.pydantic.dev"


@dlt.resource(name="agent_traces", write_disposition="replace")
def get_logfire_traces():
    headers = {"Authorization": f"Bearer {LOGFIRE_READ_TOKEN}"}
    sql = "SELECT * FROM records ORDER BY start_timestamp DESC LIMIT 1000"
    url = f"{LOGFIRE_BASE_URL}/v1/query"
    params = {"sql": sql, "format": "json"}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    # Response is columnar: {"columns": [{"name": ..., "values": [...]}, ...]}
    columns = data["columns"]
    col_names = [c["name"] for c in columns]
    col_values = [c["values"] for c in columns]

    num_rows = len(col_values[0]) if col_values else 0
    for i in range(num_rows):
        yield {col_names[j]: col_values[j][i] for j in range(len(col_names))}


@dlt.source
def logfire_source():
    return get_logfire_traces()


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="logfire_pipeline",
        destination="duckdb",
        dataset_name="agent_traces",
    )

    load_info = pipeline.run(logfire_source())
    print(load_info)

    import duckdb
    conn = duckdb.connect("logfire_pipeline.duckdb")
    result = conn.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'agent_traces'"
    ).fetchone()
    print(f"Number of tables: {result[0]}")
    conn.close()
