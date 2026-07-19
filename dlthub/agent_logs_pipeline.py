"""dlt REST API pipeline: load agent logs from test API into DuckDB."""

import dlt
from dlt.hub import run
from dlt.sources.rest_api import RESTAPIConfig, rest_api_source


def load_agent_logs() -> None:
    """Load agent logs from the test API into DuckDB.

    API serves 1,000,000 simulated Claude Code agent logs paginated by offset/limit.
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://test-agent-traces-api-xt2e7ottma-ew.a.run.app",
        },
        "resource_defaults": {
            "primary_key": "uuid",
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "logs",
                "endpoint": {
                    "path": "/logs",
                    "data_selector": "logs",
                    "params": {
                        "limit": 1000,
                    },
                    "paginator": {
                        "type": "offset",
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "limit": 1000,
                        "total_path": "total",
                    },
                },
            }
        ],
    }

    pipeline = dlt.pipeline(
        pipeline_name="agent_logs",
        destination="duckdb",
        dataset_name="agent_logs",
        dev_mode=True,
    )

    source = rest_api_source(config)

    # .add_limit(1) loads one page (1000 rows) for dev/testing
    load_info = pipeline.run(source.add_limit(1), write_disposition="replace")
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


@run.pipeline("agent_logs")
def run_agent_logs() -> None:
    """Production entry point for dltHub Platform."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://test-agent-traces-api-xt2e7ottma-ew.a.run.app",
        },
        "resource_defaults": {
            "primary_key": "uuid",
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "logs",
                "endpoint": {
                    "path": "/logs",
                    "data_selector": "logs",
                    "params": {
                        "limit": 1000,
                    },
                    "paginator": {
                        "type": "offset",
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "limit": 1000,
                        "total_path": "total",
                    },
                },
            }
        ],
    }

    pipeline = dlt.pipeline(
        pipeline_name="agent_logs",
        destination="playground",
        dataset_name="agent_logs_data",
    )

    source = rest_api_source(config)
    load_info = pipeline.run(source, write_disposition="replace")
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load_agent_logs()
