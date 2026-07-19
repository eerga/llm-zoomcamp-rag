Dlt hub lesson

# **Part 1**

See what’s available for Claude logs: 

# see if Claude files exit
ls ~/.claude/
# see which projects use Claude
ls ~/.claude/projects
# look at one of the files
cat ~/.claude/projects/-Users-I556249-PycharmProjects-llm-zoomcamp-rag/261a5453-7d3f-43b4-b4eb-5a40a849282e.jsonl
# download dlt-hub

uvx dlthub-init@latest
For virtual env: yes

# Claude request:
build dlt pipeline for my local claude logs to duckdb, load raw json into duckdb

# Question:
- Skill and tool - what’s the difference?
- Answer:
    - Skill: a way to extend your agent to give it some functionality that the developers of the agent didn't do. Describe it in the markdown file, and the agent will do it - like an instruction manual
    - Tool: a repeated function that's helpful when running your agent (so that Claude doesn't waste time building this stuff over and over again - like read_jsonl item for dlt hub)


# Ensure the pipeline is correct and ask Claude to:
- debug my pipeline

# Look at the dashboard:
uv run dlthub local show

# Ask Claude to Build a Marimo (cooler version of Jupyter notebook) Report
build a marimo report for my claude logs

# **Part 2**

# Claude request:
build dlt pipeline for my local agent logs, load data from https:/test-agent-traces-api-xt2e7ottma-ew.a.run.app/docs, logs endpoint to duckdb, and build a marimo report from this data

Part 1 explored looking at the local Claude logs and epxlored with Marimo what these logs look like

For the second part, we are trying to explore organizational logs, so we are using a fake API to mimic this work
The idea is that you can provide the API link to Claude, and we can get help with building the pipeline (using SKILLS.md) to get the report sooner (we don't have to mess with parsing the logs, pagination, etc. )

With dlt, you can load data from many data sources

1:08:42
# STOPPED
Next step is to deploy this :) 

`uv run dlthub login`

After logging in, run to get propted to the playground UI:
`uv run dlthub show`

To access the help bar:

`uv run dlthub -h`

To access a list of workspaces:

`uv run dlthub workspace list`

To deploy, ask this from Claude run this:

`deploy rest_api_pipeline.py` 
- You will be prompted to connect your work to a workspace for future deployment
- For storage options, keep DuckDB for now

You cannot deploy the dashboards with the local files - they should exist somewhere in the cloud storage

If we have some secret info, we can create a GCP project with cloud bucket, configure secret access to it, and get the data this way

# Question - why do I want to use dlt?
It's a lot of work - that's why 

Stopped watch at 1:23

Change destination in the pipeline script to `playground`

let's not forget to install deltalake dependency to `pyproject.ml`


run this code to deploy:
`uv run dlthub deploy`

and then run


