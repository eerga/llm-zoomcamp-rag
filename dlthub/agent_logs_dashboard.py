import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import dlt

    return alt, dlt, mo


@app.cell
def _(dlt):
    pipeline = dlt.attach("agent_logs")
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(mo):
    mo.md("""
    # Agent Logs Dashboard
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Message Type Distribution
    """)
    return


@app.cell
def _(dataset):
    df_chart1 = dataset("""
        SELECT type, COUNT(*) AS n
        FROM logs
        GROUP BY type
        ORDER BY n DESC
    """).df()
    return (df_chart1,)


@app.cell
def _(alt, df_chart1, mo):
    _chart = alt.Chart(df_chart1).mark_bar().encode(
        x=alt.X("type:N", sort="-y", title="Message Type"),
        y=alt.Y("n:Q", title="Count"),
        tooltip=["type:N", "n:Q"]
    ).properties(title="Message Type Distribution", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Token Usage per Session (Top 20)
    """)
    return


@app.cell
def _(dataset):
    import pandas as pd
    df_chart2_raw = dataset("""
        SELECT
            RIGHT(session_id, 8) AS session,
            SUM(usage__input_tokens) AS input_tokens,
            SUM(usage__output_tokens) AS output_tokens
        FROM logs
        WHERE usage__input_tokens IS NOT NULL
        GROUP BY session_id
        ORDER BY input_tokens DESC
        LIMIT 20
    """).df()
    df_chart2 = df_chart2_raw.melt(
        id_vars="session",
        value_vars=["input_tokens", "output_tokens"],
        var_name="token_type",
        value_name="tokens"
    )
    return (df_chart2,)


@app.cell
def _(alt, df_chart2, mo):
    _chart = alt.Chart(df_chart2).mark_bar().encode(
        x=alt.X("session:N", sort="-y", title="Session (last 8 chars)"),
        y=alt.Y("tokens:Q", title="Tokens"),
        color=alt.Color("token_type:N", title="Token Type"),
        xOffset="token_type:N",
        tooltip=["session:N", "token_type:N", "tokens:Q"]
    ).properties(title="Token Usage per Session (Top 20)", width=600, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Messages Over Time
    """)
    return


@app.cell
def _(dataset):
    df_chart3 = dataset("""
        SELECT
            DATE_TRUNC('minute', timestamp) AS minute,
            COUNT(*) AS message_count
        FROM logs
        WHERE timestamp IS NOT NULL
        GROUP BY 1
        ORDER BY 1
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3, mo):
    _chart = alt.Chart(df_chart3).mark_line(point=True).encode(
        x=alt.X("minute:T", title="Time"),
        y=alt.Y("message_count:Q", title="Messages"),
        tooltip=["minute:T", "message_count:Q"]
    ).properties(title="Messages Over Time (per Minute)", width=600, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Tool Usage Breakdown
    """)
    return


@app.cell
def _(dataset):
    df_chart4 = dataset("""
        SELECT name AS tool, COUNT(*) AS uses
        FROM logs__message__content
        WHERE type = 'tool_use'
        GROUP BY name
        ORDER BY uses DESC
    """).df()
    return (df_chart4,)


@app.cell
def _(alt, df_chart4, mo):
    _chart = alt.Chart(df_chart4).mark_bar().encode(
        x=alt.X("uses:Q", title="Times Used"),
        y=alt.Y("tool:N", sort="-x", title="Tool"),
        tooltip=["tool:N", "uses:Q"]
    ).properties(title="Tool Usage Breakdown", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Conversation Depth by Session (Top 20)
    """)
    return


@app.cell
def _(dataset):
    df_chart5 = dataset("""
        SELECT RIGHT(session_id, 8) AS session, COUNT(*) AS message_count
        FROM logs
        WHERE session_id IS NOT NULL
        GROUP BY session_id
        ORDER BY message_count DESC
        LIMIT 20
    """).df()
    return (df_chart5,)


@app.cell
def _(alt, df_chart5, mo):
    _chart = alt.Chart(df_chart5).mark_bar().encode(
        x=alt.X("session:N", sort="-y", title="Session (last 8 chars)"),
        y=alt.Y("message_count:Q", title="Messages"),
        tooltip=["session:N", "message_count:Q"]
    ).properties(title="Conversation Depth by Session (Top 20)", width=600, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Output Token Distribution (Assistant Messages)
    """)
    return


@app.cell
def _(dataset):
    df_chart6 = dataset("""
        SELECT usage__output_tokens AS output_tokens
        FROM logs
        WHERE usage__output_tokens IS NOT NULL
          AND message__role = 'assistant'
    """).df()
    return (df_chart6,)


@app.cell
def _(alt, df_chart6, mo):
    _chart = alt.Chart(df_chart6).mark_bar().encode(
        x=alt.X("output_tokens:Q", bin=alt.Bin(maxbins=30), title="Output Tokens"),
        y=alt.Y("count():Q", title="Messages"),
        tooltip=["count():Q"]
    ).properties(title="Output Token Distribution (Assistant Messages)", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Input vs Output Token Ratio per Session
    """)
    return


@app.cell
def _(dataset):
    df_chart7 = dataset("""
        SELECT
            RIGHT(session_id, 8) AS session,
            SUM(usage__input_tokens) AS input_tokens,
            SUM(usage__output_tokens) AS output_tokens,
            ROUND(SUM(usage__output_tokens)::FLOAT / NULLIF(SUM(usage__input_tokens), 0), 3) AS output_input_ratio
        FROM logs
        WHERE usage__input_tokens IS NOT NULL
        GROUP BY session_id
        ORDER BY output_input_ratio DESC
        LIMIT 20
    """).df()
    return (df_chart7,)


@app.cell
def _(alt, df_chart7, mo):
    _chart = alt.Chart(df_chart7).mark_point(size=80, filled=True).encode(
        x=alt.X("input_tokens:Q", title="Input Tokens"),
        y=alt.Y("output_tokens:Q", title="Output Tokens"),
        tooltip=["session:N", "input_tokens:Q", "output_tokens:Q", "output_input_ratio:Q"]
    ).properties(title="Input vs Output Tokens per Session (Top 20)", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


if __name__ == "__main__":
    app.run()
