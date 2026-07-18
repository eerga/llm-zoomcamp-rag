"""dlt filesystem pipeline: load Claude session logs (JSONL) into DuckDB."""

import dlt
from dlt.sources.filesystem import filesystem, read_jsonl


def load_messages() -> None:
    """Load Claude JSONL session logs into DuckDB.

    bucket_url is read from .dlt/config.toml under [sources.filesystem].
    """
    pipeline = dlt.pipeline(
        pipeline_name="claude_logs",
        destination="duckdb",
        dataset_name="claude_logs",
        dev_mode=True,
    )

    reader = (filesystem(file_glob="*.jsonl") | read_jsonl()).with_name("messages")

    load_info = pipeline.run(reader, write_disposition="replace")
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load_messages()
