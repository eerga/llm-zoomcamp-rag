# Analysis Plan: claude_logs

## Connection
- **Pipeline name**: claude_logs
- **Dataset**: claude_logs_20260718031608
- **Destination**: duckdb (`.dlt/data/dev/claude_logs.duckdb`)

## Profile Summary
- **messages**: 1180 rows, 7 sessions, date range 2026-06-21 → 2026-07-18
- **messages__message__content**: 629 rows (tool calls + content blocks)
- Key numeric columns: `message__usage__input_tokens`, `message__usage__output_tokens`, `message__usage__cache_read_input_tokens`
- Key categorical: `type` (10 values), `message__role` (user/assistant), `message__model` (claude-sonnet-4-6 only)
- Tool usage tracked in `messages__message__content` where `type = 'tool_use'`, column `name`

## Questions
- [x] Token usage by session (input vs output tokens)
- [x] Messages over time (message count by date)
- [x] Tool usage breakdown (which tools used most)
- [x] Cache efficiency (input vs cache-read tokens per session)
- [x] Conversation depth (messages per session)
- [x] Message type distribution (all type values)
- [x] Output tokens per assistant message (response size distribution)

---

## Chart 1: Token Usage by Session
**Question**: Which sessions consumed the most input and output tokens?
**Type**: Grouped bar chart
**X**: session_id (shortened to last 8 chars) — nominal
**Y**: tokens — quantitative
**Color**: token_type (input / output)
**Source**: messages

```sql
SELECT
    RIGHT(session_id, 8) AS session,
    SUM(message__usage__input_tokens) AS input_tokens,
    SUM(message__usage__output_tokens) AS output_tokens
FROM messages
WHERE message__usage__input_tokens IS NOT NULL
GROUP BY session_id
ORDER BY input_tokens DESC
```

```python
import altair as alt

df = dataset("SELECT RIGHT(session_id, 8) AS session, SUM(message__usage__input_tokens) AS input_tokens, SUM(message__usage__output_tokens) AS output_tokens FROM messages WHERE message__usage__input_tokens IS NOT NULL GROUP BY session_id ORDER BY input_tokens DESC").df()

melted = df.melt(id_vars="session", value_vars=["input_tokens", "output_tokens"], var_name="token_type", value_name="tokens")

chart1 = alt.Chart(melted).mark_bar().encode(
    x=alt.X("session:N", title="Session (last 8 chars)", sort="-y"),
    y=alt.Y("tokens:Q", title="Tokens"),
    color=alt.Color("token_type:N", title="Token Type"),
    xOffset="token_type:N",
    tooltip=["session:N", "token_type:N", "tokens:Q"]
).properties(title="Token Usage by Session", width=500, height=300)
```

---

## Chart 2: Messages Over Time
**Question**: How many messages were sent each day?
**Type**: Line chart
**X**: date — temporal
**Y**: COUNT(*) — quantitative
**Source**: messages

```sql
SELECT
    DATE_TRUNC('day', timestamp) AS date,
    COUNT(*) AS message_count
FROM messages
WHERE timestamp IS NOT NULL
GROUP BY 1
ORDER BY 1
```

```python
import altair as alt

df = dataset("SELECT DATE_TRUNC('day', timestamp) AS date, COUNT(*) AS message_count FROM messages WHERE timestamp IS NOT NULL GROUP BY 1 ORDER BY 1").df()

chart2 = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("message_count:Q", title="Messages"),
    tooltip=["date:T", "message_count:Q"]
).properties(title="Messages Over Time (Daily)", width=500, height=300)
```

---

## Chart 3: Tool Usage Breakdown
**Question**: Which tools were used most frequently?
**Type**: Horizontal bar chart
**X**: COUNT(*) — quantitative
**Y**: name — nominal
**Source**: messages__message__content

```sql
SELECT
    name AS tool,
    COUNT(*) AS uses
FROM messages__message__content
WHERE type = 'tool_use'
GROUP BY name
ORDER BY uses DESC
```

```python
import altair as alt

df = dataset("SELECT name AS tool, COUNT(*) AS uses FROM messages__message__content WHERE type = 'tool_use' GROUP BY name ORDER BY uses DESC").df()

chart3 = alt.Chart(df).mark_bar().encode(
    x=alt.X("uses:Q", title="Times Used"),
    y=alt.Y("tool:N", sort="-x", title="Tool"),
    tooltip=["tool:N", "uses:Q"]
).properties(title="Tool Usage Breakdown", width=500, height=300)
```

---

## Chart 4: Cache Efficiency by Session
**Question**: How much did prompt caching save per session?
**Type**: Grouped bar chart
**X**: session — nominal
**Y**: tokens — quantitative
**Color**: token_type (input / cache_read)
**Source**: messages

```sql
SELECT
    RIGHT(session_id, 8) AS session,
    SUM(message__usage__input_tokens) AS input_tokens,
    SUM(message__usage__cache_read_input_tokens) AS cache_read_tokens
FROM messages
WHERE message__usage__input_tokens IS NOT NULL
GROUP BY session_id
ORDER BY input_tokens DESC
```

```python
import altair as alt

df = dataset("SELECT RIGHT(session_id, 8) AS session, SUM(message__usage__input_tokens) AS input_tokens, SUM(message__usage__cache_read_input_tokens) AS cache_read_tokens FROM messages WHERE message__usage__input_tokens IS NOT NULL GROUP BY session_id ORDER BY input_tokens DESC").df()

melted = df.melt(id_vars="session", value_vars=["input_tokens", "cache_read_tokens"], var_name="token_type", value_name="tokens")

chart4 = alt.Chart(melted).mark_bar().encode(
    x=alt.X("session:N", title="Session (last 8 chars)", sort="-y"),
    y=alt.Y("tokens:Q", title="Tokens"),
    color=alt.Color("token_type:N", title="Type"),
    xOffset="token_type:N",
    tooltip=["session:N", "token_type:N", "tokens:Q"]
).properties(title="Cache Efficiency by Session", width=500, height=300)
```

---

## Chart 5: Conversation Depth (Messages per Session)
**Question**: How deep were each session's conversations?
**Type**: Bar chart
**X**: session — nominal
**Y**: message_count — quantitative
**Source**: messages

```sql
SELECT
    RIGHT(session_id, 8) AS session,
    COUNT(*) AS message_count
FROM messages
WHERE session_id IS NOT NULL
GROUP BY session_id
ORDER BY message_count DESC
```

```python
import altair as alt

df = dataset("SELECT RIGHT(session_id, 8) AS session, COUNT(*) AS message_count FROM messages WHERE session_id IS NOT NULL GROUP BY session_id ORDER BY message_count DESC").df()

chart5 = alt.Chart(df).mark_bar().encode(
    x=alt.X("session:N", sort="-y", title="Session (last 8 chars)"),
    y=alt.Y("message_count:Q", title="Messages"),
    tooltip=["session:N", "message_count:Q"]
).properties(title="Conversation Depth by Session", width=500, height=300)
```

---

## Chart 6: Message Type Distribution
**Question**: What is the breakdown of message types?
**Type**: Bar chart
**X**: type — nominal
**Y**: COUNT(*) — quantitative
**Source**: messages

```sql
SELECT
    type,
    COUNT(*) AS n
FROM messages
GROUP BY type
ORDER BY n DESC
```

```python
import altair as alt

df = dataset("SELECT type, COUNT(*) AS n FROM messages GROUP BY type ORDER BY n DESC").df()

chart6 = alt.Chart(df).mark_bar().encode(
    x=alt.X("type:N", sort="-y", title="Message Type"),
    y=alt.Y("n:Q", title="Count"),
    tooltip=["type:N", "n:Q"]
).properties(title="Message Type Distribution", width=500, height=300)
```

---

## Chart 7: Output Token Distribution (Assistant Messages)
**Question**: How are assistant response sizes distributed?
**Type**: Histogram
**X**: output_tokens (binned) — quantitative
**Y**: COUNT(*) — quantitative
**Source**: messages

```sql
SELECT
    message__usage__output_tokens AS output_tokens
FROM messages
WHERE message__usage__output_tokens IS NOT NULL
  AND message__role = 'assistant'
```

```python
import altair as alt

df = dataset("SELECT message__usage__output_tokens AS output_tokens FROM messages WHERE message__usage__output_tokens IS NOT NULL AND message__role = 'assistant'").df()

chart7 = alt.Chart(df).mark_bar().encode(
    x=alt.X("output_tokens:Q", bin=alt.Bin(maxbins=30), title="Output Tokens"),
    y=alt.Y("count():Q", title="Messages"),
    tooltip=["count():Q"]
).properties(title="Output Token Distribution (Assistant Messages)", width=500, height=300)
```
