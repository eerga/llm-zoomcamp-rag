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
    pipeline = dlt.attach("claude_logs")
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(mo):
    mo.md("""
    # Claude Logs Dashboard
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Token Usage by Session
    """)
    return


@app.cell
def _(dataset):
    import pandas as pd
    df_chart1_raw = dataset("""
        SELECT
            RIGHT(session_id, 8) AS session,
            SUM(message__usage__input_tokens) AS input_tokens,
            SUM(message__usage__output_tokens) AS output_tokens
        FROM messages
        WHERE message__usage__input_tokens IS NOT NULL
        GROUP BY session_id
        ORDER BY input_tokens DESC
    """).df()
    df_chart1 = df_chart1_raw.melt(
        id_vars="session",
        value_vars=["input_tokens", "output_tokens"],
        var_name="token_type",
        value_name="tokens"
    )
    return (df_chart1,)


@app.cell
def _(alt, df_chart1, mo):
    _chart = alt.Chart(df_chart1).mark_bar().encode(
        x=alt.X("session:N", title="Session (last 8 chars)", sort="-y"),
        y=alt.Y("tokens:Q", title="Tokens"),
        color=alt.Color("token_type:N", title="Token Type"),
        xOffset="token_type:N",
        tooltip=["session:N", "token_type:N", "tokens:Q"]
    ).properties(title="Token Usage by Session", width=500, height=300)
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
    df_chart2 = dataset("""
        SELECT
            DATE_TRUNC('day', timestamp) AS date,
            COUNT(*) AS message_count
        FROM messages
        WHERE timestamp IS NOT NULL
        GROUP BY 1
        ORDER BY 1
    """).df()
    return (df_chart2,)


@app.cell
def _(alt, df_chart2, mo):
    _chart = alt.Chart(df_chart2).mark_line(point=True).encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("message_count:Q", title="Messages"),
        tooltip=["date:T", "message_count:Q"]
    ).properties(title="Messages Over Time (Daily)", width=500, height=300)
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
    df_chart3 = dataset("""
        SELECT
            name AS tool,
            COUNT(*) AS uses
        FROM messages__message__content
        WHERE type = 'tool_use'
        GROUP BY name
        ORDER BY uses DESC
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3, mo):
    _chart = alt.Chart(df_chart3).mark_bar().encode(
        x=alt.X("uses:Q", title="Times Used"),
        y=alt.Y("tool:N", sort="-x", title="Tool"),
        tooltip=["tool:N", "uses:Q"]
    ).properties(title="Tool Usage Breakdown", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Cache Efficiency by Session
    """)
    return


@app.cell
def _(dataset):
    df_chart4_raw = dataset("""
        SELECT
            RIGHT(session_id, 8) AS session,
            SUM(message__usage__input_tokens) AS input_tokens,
            SUM(message__usage__cache_read_input_tokens) AS cache_read_tokens
        FROM messages
        WHERE message__usage__input_tokens IS NOT NULL
        GROUP BY session_id
        ORDER BY input_tokens DESC
    """).df()
    df_chart4 = df_chart4_raw.melt(
        id_vars="session",
        value_vars=["input_tokens", "cache_read_tokens"],
        var_name="token_type",
        value_name="tokens"
    )
    return (df_chart4,)


@app.cell
def _(alt, df_chart4, mo):
    _chart = alt.Chart(df_chart4).mark_bar().encode(
        x=alt.X("session:N", title="Session (last 8 chars)", sort="-y"),
        y=alt.Y("tokens:Q", title="Tokens"),
        color=alt.Color("token_type:N", title="Type"),
        xOffset="token_type:N",
        tooltip=["session:N", "token_type:N", "tokens:Q"]
    ).properties(title="Cache Efficiency by Session", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Conversation Depth by Session
    """)
    return


@app.cell
def _(dataset):
    df_chart5 = dataset("""
        SELECT
            RIGHT(session_id, 8) AS session,
            COUNT(*) AS message_count
        FROM messages
        WHERE session_id IS NOT NULL
        GROUP BY session_id
        ORDER BY message_count DESC
    """).df()
    return (df_chart5,)


@app.cell
def _(alt, df_chart5, mo):
    _chart = alt.Chart(df_chart5).mark_bar().encode(
        x=alt.X("session:N", sort="-y", title="Session (last 8 chars)"),
        y=alt.Y("message_count:Q", title="Messages"),
        tooltip=["session:N", "message_count:Q"]
    ).properties(title="Conversation Depth by Session", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Message Type Distribution
    """)
    return


@app.cell
def _(dataset):
    df_chart6 = dataset("""
        SELECT
            type,
            COUNT(*) AS n
        FROM messages
        GROUP BY type
        ORDER BY n DESC
    """).df()
    return (df_chart6,)


@app.cell
def _(alt, df_chart6, mo):
    _chart = alt.Chart(df_chart6).mark_bar().encode(
        x=alt.X("type:N", sort="-y", title="Message Type"),
        y=alt.Y("n:Q", title="Count"),
        tooltip=["type:N", "n:Q"]
    ).properties(title="Message Type Distribution", width=500, height=300)
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
    df_chart7 = dataset("""
        SELECT
            message__usage__output_tokens AS output_tokens
        FROM messages
        WHERE message__usage__output_tokens IS NOT NULL
          AND message__role = 'assistant'
    """).df()
    return (df_chart7,)


@app.cell
def _(alt, df_chart7, mo):
    _chart = alt.Chart(df_chart7).mark_bar().encode(
        x=alt.X("output_tokens:Q", bin=alt.Bin(maxbins=30), title="Output Tokens"),
        y=alt.Y("count():Q", title="Messages"),
        tooltip=["count():Q"]
    ).properties(title="Output Token Distribution (Assistant Messages)", width=500, height=300)
    mo.ui.altair_chart(_chart)
    return


if __name__ == "__main__":
    app.run()
