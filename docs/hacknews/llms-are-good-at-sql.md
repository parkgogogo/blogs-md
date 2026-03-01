---
title: "LLMs Are Good at SQL. We Gave Ours Terabytes of CI Logs."
url: "https://www.mendral.com/blog/llms-are-good-at-sql"
rating: 9
category: "AI/ML & DevOps"
date: "2026-02-28"
---

# LLMs Are Good at SQL. We Gave Ours Terabytes of CI Logs.

Last week, our agent traced a flaky test to a dependency bump three weeks prior. It did this by writing its own SQL queries, scanning hundreds of millions of log lines across a dozen queries, and following a trail from job metadata to raw log output. The whole investigation took seconds.

To do this, the agent needs context: not one log file, but every build, every test, every log line, across months of history. Every week, about **1.5 billion CI log lines** and **700K jobs** flow through our system. All of it lands in ClickHouse, compressed at 35:1. All of it is queryable in milliseconds.

## A SQL interface for the agent

We expose a SQL interface to the agent, scoped to the organization it's investigating. The agent constructs its own queries based on the question. No predefined query library, no rigid tool API.

LLMs are good at SQL. There's an enormous amount of SQL in training data, and the syntax maps well to natural-language questions about data. A constrained tool API like `get_failure_rate(workflow, days)` would limit the agent to the questions we anticipated. A SQL interface lets it ask questions we never thought of, which matters when you're debugging novel failures.

The agent queries two main targets:

**Job metadata**: a materialized view with one row per CI job execution. The agent uses this 63% of the time for questions like "how often does this fail?", "what's the success rate?", "which jobs are slowest?", "when did this start failing?"

**Raw log lines**: one row per log line. The agent uses this 37% of the time for questions like "show me the error output for this job", "when did this log pattern first appear?", "how often does this error message occur across runs?"

### 52,000 queries across 8,500 investigations

We analyzed 8,534 agent sessions and 52,312 queries from our observability pipeline.

The agent doesn't stop at one query. It investigates. Starts broad, then drills in. Total rows scanned across all queries to answer one question:

| Target | Sessions | Avg queries | Median rows | P75 | P95 |
|--------|----------|-------------|-------------|-----|-----|
| Job metadata | 8,210 | 4.0 | **164K** | 563K | 4.4M |
| Raw log lines | 5,413 | 3.5 | **4.4M** | 69M | 4.3B |
| **Combined** | **8,534** | **4.4** | **335K** | **5.2M** | **940M** |

The typical question scans **335K rows** across about 3 queries. At P75 it's 5.2 million rows. At P95 it's **940 million rows**. The heaviest raw-log sessions, deep investigations tracing error patterns across months of history, scan **4.3 billion rows**.

### The search pattern

The agent starts broad and narrows. A typical investigation begins with job metadata: "what's the failure rate for this workflow?", "which jobs failed on this commit?" These are cheap queries (median 47K rows) against a compact, pre-aggregated materialized view.

When it finds something interesting, it drills into raw logs: "show me the stack trace for this specific failure", "has this error message appeared before?" These are the expensive queries (median 1.1M rows), full-text scans across log output. But this is exactly the kind of search that would take a human minutes of scrolling through GitHub Actions log viewers.

The agent averages 4.4 queries per session, but heavy investigations issue many more. A P95 session isn't one big query. It's the agent following a trail, query after query, as it narrows in on a root cause.

## 5 TiB uncompressed, 154 GiB on disk

For the agent to query this fast, the data needs to be structured for it. Up to 300 million log lines flow through on a busy day. We use ClickHouse.

### The denormalization bet

Every log line in our system carries **48 columns** of metadata: the full context of the CI run it belongs to. Commit SHA, author, branch, PR title, workflow name, job name, step name, runner info, timestamps, and more.

In a traditional row-store, this would be insane. You'd normalize. Run-level metadata in one table, job metadata in another, join at query time. Denormalizing 48 columns onto every single log line sounds like a storage disaster.

In ClickHouse's columnar format, it's essentially free.

A column like `commit_message` has the same value for every log line in a CI run, and a single run can produce thousands of log lines. ClickHouse stores those thousands of identical values in sequence. The compression algorithm sees the repetition and compresses it to almost nothing.

| Column | Compression ratio | Why |
|--------|-------------------|-----|
| `commit_message` | **301:1** | Same message for every line in a run (thousands of lines) |
| `display_title` | **160:1** | Same PR/commit title across all lines |
| `workflow_path` | **79:1** | Same `.github/workflows/foo.yml` path |
| `step_name` | **52:1** | Same step name across hundreds of lines |
| `job_name` | **48:1** | Same job name across hundreds/thousands of lines |

The agent asks arbitrary questions. One might filter by commit author, the next by runner label, the next by step name. Without denormalization, every one of those requires a join. With it, they're all column predicates.

### The numbers

| Layer | Size |
|-------|------|
| Raw log text (`line_content` uncompressed) | 664 GiB |
| All 48 columns uncompressed | 5.31 TiB |
| On disk (compressed) | **154 GiB** |
| **Compression ratio** | **35:1** |

The raw log text alone is 664 GiB. Adding all 48 columns of metadata inflates it to 5.31 TiB uncompressed, 8x the raw text. On disk, the whole thing compresses to 154 GiB. ClickHouse stores 8x more data (all the enriched metadata) in a quarter of the size of the raw text alone.

That's about **21 bytes per log line** on disk, including all 48 columns. Yes, really. 21 bytes for a log line plus its commit SHA, author, branch, job name, step name, runner info, and 41 other fields.

### Where the storage actually goes

Not all columns compress equally. The unique-per-row columns (log text, timestamp, line number) compress modestly and dominate storage. The metadata columns, which repeat across thousands of lines, are nearly free.

| Column | On disk | % of total | Compression ratio |
|--------|---------|------------|-------------------|
| `line_content` (log text) | 53.2 GiB | 34.7% | 12.5:1 |
| `ts` (nanosecond timestamp) | 15.7 GiB | 10.2% | 3.7:1 |
| `line_number` | 12.4 GiB | 8.1% | 2.3:1 |
| `job_name` | 8.2 GiB | 5.4% | 48:1 |
| `runner_name` | 4.5 GiB | 2.9% | 31:1 |
| `job_id` | 3.9 GiB | 2.5% | 15:1 |
| `runner_labels` | 3.8 GiB | 2.5% | 52:1 |
| Everything else (41 columns) | ~51 GiB | ~33% | varies |

The top three (`line_content`, `ts`, `line_number`) account for 53% of all storage. Everything else is repeated metadata that compresses to almost nothing.

### Query performance

We use a few ClickHouse patterns that keep things fast:

**Primary key design** means the data is physically sorted for our access pattern. The sort order is `(org, ts, repository, run_id, ...)`, so every query is scoped to one organization and a time range, and ClickHouse skips everything else without reading it.

**Skip indexes** let ClickHouse avoid scanning data it doesn't need. We use bloom filters on 14 columns (org, repository, job name, branch, commit SHA, etc.) and an ngram bloom filter on `line_content` for full-text search. When the agent searches for an error message across billions of log lines, ClickHouse checks the ngram index to skip granules that can't contain the search term, turning a full table scan into a targeted read.

**Materialized views** pre-compute aggregations on insert. When the agent asks "what's the failure rate for this workflow over the last 30 days?", the answer is already computed. The aggregation happened when the data was written.

**Async inserts** give us high write throughput without building our own batching layer. We fire-and-forget individual inserts, and ClickHouse batches them internally.

Query latency across 52K queries:

| Target | Queries | Median | P75 | P95 |
|--------|---------|--------|-----|-----|
| Job metadata | 33K | **20ms** | 30ms | 80ms |
| Raw log lines | 19K | **110ms** | 780ms | 18.1s |

Job metadata queries return in 20ms at the median. Raw log queries, scanning a million rows at the median, come back in 110ms.

Latency scales roughly linearly with rows scanned:

| Rows scanned | Queries | Median latency | P95 latency |
|--------------|---------|----------------|-------------|
| < 1K | 1,621 | 10ms | 50ms |
| 1K-10K | 2,608 | 20ms | 50ms |
| 10K-100K | 27,044 | 20ms | 50ms |
| 100K-1M | 8,515 | 40ms | 390ms |
| 1M-10M | 7,199 | 90ms | 1.2s |
| 10M-100M | 2,630 | 690ms | 6.8s |
| 100M-1B | 1,814 | 6.8s | 30.6s |
| 1B+ | 1,029 | 31s | 82s |

10x more rows ≈ 10x more latency. 60% of all queries scan under 100K rows and return in under 50ms, fast enough that the agent can fire off several per second without breaking stride. At the extreme end, the agent occasionally scans over a billion rows in a single query; even those complete in about 30 seconds at the median.

## Ingesting through GitHub's rate limit

None of the above works without fresh data. The agent needs to reason about the build that just failed, not one from an hour ago.

### The rate limit constraint

GitHub's API gives you 15,000 requests per hour per App installation (5,000 on non-Enterprise plans). That sounds generous until you're continuously polling workflow runs, jobs, steps, and log output across dozens of active repositories. A single commit can spawn hundreds of parallel jobs, each producing logs you need to fetch.

And ingestion isn't the only thing hitting the API. When the agent investigates a failure, it pulls PR metadata, reads file diffs, posts comments, and opens pull requests. All of that counts against the same 15,000-request budget. **Throttle ingestion too aggressively and your data goes stale. Throttle too little and you starve the agent of the API access it needs to do its job.**

Early on, we hit this. Our ingestion would slam into the rate limit, get blocked for the remainder of the hour, and fall behind. By the time it caught up, we were ingesting logs from 30+ minutes ago. For an agent that needs to reason about the build that just failed, that's useless. If an engineer has to wait for the agent to catch up, they've already context-switched to investigating manually.

The fix was throttling: spreading requests evenly across the rate limit window instead of bursting. We cap ingestion at roughly 3 requests per second, keeping about 4,000 requests per hour free for the agent.

Once we trusted the throttling, we pushed the ingestion rate about 20% higher. The budget draws down more aggressively after the change. We're consuming more of the available headroom per window, while still never fully exhausting it. Fresher data, acceptable margin.

We target under **5 minutes at P95** for ingestion delay, the time between an event happening on GitHub and it being queryable in our system. Most of the time, we're at a few seconds.

### Durable execution

Both our ingestion pipeline and our agent run on Inngest, a durable execution engine. When either one hits a rate limit, it doesn't crash, retry blindly, or spin in a loop. It **suspends**.

GitHub's rate limit response headers tell you exactly how long you need to wait. We read that value, add 10% jitter to avoid a thundering herd when the limit resets, and suspend the execution. The full state is checkpointed: progress through the workflow, which jobs have been fetched, where we are in the log pagination.

When the wait is over, execution resumes at exactly the point it left off. No re-initialization, no duplicate work. It picks up the next API call as if nothing happened.

Compare this to the alternative: retry logic, state recovery, deduplication. Every function needs to be idempotent. Every interrupted batch needs to be reconciled. With durable execution, the rate limit is just a pause button.

### Absorbing traffic spikes

CI activity is bursty. Someone merges a big PR, a release branch gets cut, three teams push at the same time.

The queued work spikes to 3,000+ during bursts of CI activity. The execution engine absorbs the spikes and processes work at a steady rate.

Spikes during peak activity, but the system recovers. The 5-minute P95 target holds: bursts push delay up briefly, then it drops back to seconds once the queue drains.

Nobody puts "we built a really good rate limiter" on their landing page. But without fresh, queryable data, your agent can't answer the question that actually matters: did I break this, or was it already broken?

---

*We're building Mendral (YC W26). We spent a decade building and scaling CI systems at Docker and Dagger, and the work was always the same: stare at logs, correlate failures, figure out what changed. Now we're automating it.*

---

# 中文翻译

上周，我们的 Agent 追踪到了一个不稳定测试（flaky test）的根源——三周前的一次依赖更新。它通过自主编写 SQL 查询，在十几个查询中扫描了数亿行日志，顺着从任务元数据到原始日志输出的线索完成了整个调查。整个过程仅用了几秒钟。

要做到这一点，Agent 需要上下文：不是单个日志文件，而是每一次构建、每一次测试、每一行日志，跨越数月的历史数据。每周，大约有 **15 亿行 CI 日志** 和 **70 万个任务** 流经我们的系统。所有这些数据都进入 ClickHouse，以 35:1 的比率压缩。所有数据都可以在毫秒级内查询。

## 为 Agent 提供 SQL 接口

我们为 Agent 暴露了一个 SQL 接口，范围限定在它正在调查的组织内。Agent 根据问题自主构建查询。没有预定义的查询库，没有僵化的工具 API。

LLM 擅长 SQL。训练数据中有海量的 SQL 内容，而且 SQL 语法与自然语言的数据问题映射得很好。像 `get_failure_rate(workflow, days)` 这样受限的工具 API 会将 Agent 限制在我们预期的问题上。而 SQL 接口让它能够提出我们从未想过的问题，这在调试新型故障时至关重要。

Agent 主要查询两个目标：

**任务元数据（Job metadata）**：一个物化视图，每行代表一次 CI 任务执行。Agent 63% 的时间使用它来回答诸如"这个多久失败一次？"、"成功率是多少？"、"哪些任务最慢？"、"什么时候开始失败的？"等问题。

**原始日志行（Raw log lines）**：每行代表一行日志。Agent 37% 的时间使用它来回答诸如"显示这个任务的错误输出"、"这个日志模式什么时候首次出现？"、"这个错误消息在多次运行中出现的频率？"等问题。

### 8,500 次调查中的 52,000 次查询

我们分析了来自可观测性管道的 8,534 个 Agent 会话和 52,312 次查询。

Agent 不会止步于一次查询。它会调查。从宽泛开始，然后深入挖掘。回答一个问题时扫描的总行数：

| 目标 | 会话数 | 平均查询数 | 中位数行数 | P75 | P95 |
|------|--------|------------|------------|-----|-----|
| 任务元数据 | 8,210 | 4.0 | **164K** | 563K | 4.4M |
| 原始日志行 | 5,413 | 3.5 | **4.4M** | 69M | 4.3B |
| **合计** | **8,534** | **4.4** | **335K** | **5.2M** | **940M** |

典型问题扫描约 **33.5 万行**，使用约 3 次查询。在 P75 时达到 520 万行，在 P95 时达到 **9.4 亿行**。最重的原始日志会话——深入调查跨越数月历史的错误模式——扫描 **43 亿行**。

### 搜索模式

Agent 从宽泛开始，然后收窄。典型调查从任务元数据开始："这个工作流的成功率是多少？"、"这个提交上哪些任务失败了？"这些是廉价查询（中位数 4.7 万行），针对紧凑的预聚合物化视图。

当它发现有趣的内容时，会深入原始日志："显示这个特定失败的堆栈跟踪"、"这个错误消息以前出现过吗？"这些是昂贵的查询（中位数 110 万行），对日志输出进行全文扫描。但这正是人类需要花费数分钟在 GitHub Actions 日志查看器中滚动搜索的工作。

Agent 平均每次会话 4.4 次查询，但繁重的调查会发出更多。P95 会话不是一次大查询，而是 Agent 在缩小根本原因范围时一个接一个地跟踪线索。

## 5 TiB 未压缩，154 GiB 磁盘空间

为了让 Agent 如此快速地查询，数据需要为其结构化。繁忙的一天可能有 3 亿行日志流经系统。我们使用 ClickHouse。

### 反规范化赌注

我们系统中的每行日志都携带 **48 列** 元数据：它所属 CI 运行的完整上下文。提交 SHA、作者、分支、PR 标题、工作流名称、任务名称、步骤名称、运行器信息、时间戳等等。

在传统行式存储中，这会很疯狂。你会规范化。运行级元数据在一个表，任务元数据在另一个表，查询时进行 Join。将 48 列反规范化到每行日志上听起来像是存储灾难。

在 ClickHouse 的列式格式中，这基本上是免费的。

像 `commit_message` 这样的列在 CI 运行的每行日志中具有相同的值，单次运行可以产生数千行日志。ClickHouse 将数千个相同的值顺序存储。压缩算法看到重复后将其压缩到几乎为零。

| 列 | 压缩比 | 原因 |
|----|--------|------|
| `commit_message` | **301:1** | 运行中的每行消息相同（数千行） |
| `display_title` | **160:1** | 所有行的 PR/提交标题相同 |
| `workflow_path` | **79:1** | 相同的 `.github/workflows/foo.yml` 路径 |
| `step_name` | **52:1** | 数百行的步骤名称相同 |
| `job_name` | **48:1** | 数百/数千行的任务名称相同 |

Agent 提出任意问题。一个可能按提交作者过滤，下一个按运行器标签过滤，再下一个按步骤名称过滤。没有反规范化，每一个都需要 Join。有了它，它们都是列谓词。

### 数据详情

| 层级 | 大小 |
|------|------|
| 原始日志文本（`line_content` 未压缩） | 664 GiB |
| 全部 48 列未压缩 | 5.31 TiB |
| 磁盘上（压缩后） | **154 GiB** |
| **压缩比** | **35:1** |

仅原始日志文本就有 664 GiB。添加所有 48 列元数据后未压缩膨胀到 5.31 TiB，是原始文本的 8 倍。在磁盘上，整个数据压缩到 154 GiB。ClickHouse 存储的数据多了 8 倍（所有丰富的元数据），却只占用原始文本四分之一的空间。

这大约是磁盘上 **每行日志 21 字节**，包括全部 48 列。是的，真的。21 字节存储一行日志及其提交 SHA、作者、分支、任务名称、步骤名称、运行器信息和另外 41 个字段。

### 存储实际去向

并非所有列的压缩效果都相同。每行唯一的列（日志文本、时间戳、行号）压缩适中并主导存储。在数千行中重复的元数据列几乎免费。

| 列 | 磁盘占用 | 占总比 | 压缩比 |
|----|----------|--------|--------|
| `line_content`（日志文本） | 53.2 GiB | 34.7% | 12.5:1 |
| `ts`（纳秒时间戳） | 15.7 GiB | 10.2% | 3.7:1 |
| `line_number` | 12.4 GiB | 8.1% | 2.3:1 |
| `job_name` | 8.2 GiB | 5.4% | 48:1 |
| `runner_name` | 4.5 GiB | 2.9% | 31:1 |
| `job_id` | 3.9 GiB | 2.5% | 15:1 |
| `runner_labels` | 3.8 GiB | 2.5% | 52:1 |
| 其他（41 列） | ~51 GiB | ~33% | 各不相同 |

前三名（`line_content`、`ts`、`line_number`）占所有存储的 53%。其他都是重复元数据，压缩到几乎为零。

### 查询性能

我们使用一些 ClickHouse 模式来保持快速：

**主键设计** 意味着数据在物理上按我们的访问模式排序。排序顺序是 `(org, ts, repository, run_id, ...)`，因此每个查询都限定在一个组织和一个时间范围内，ClickHouse 无需读取就能跳过其他所有内容。

**跳数索引（Skip indexes）** 让 ClickHouse 避免扫描不需要的数据。我们在 14 列上使用布隆过滤器（组织、仓库、任务名称、分支、提交 SHA 等），并在 `line_content` 上使用 ngram 布隆过滤器进行全文搜索。当 Agent 在数十亿行日志中搜索错误消息时，ClickHouse 检查 ngram 索引以跳过不可能包含搜索词的粒度，将全表扫描转化为针对性读取。

**物化视图** 在插入时预计算聚合。当 Agent 问"这个工作流过去 30 天的失败率是多少？"时，答案已经计算好了。聚合在数据写入时就已经完成。

**异步插入** 让我们无需构建自己的批处理层就能获得高写入吞吐量。我们即发即弃单个插入，ClickHouse 内部进行批处理。

跨越 52K 查询的查询延迟：

| 目标 | 查询数 | 中位数 | P75 | P95 |
|------|--------|--------|-----|-----|
| 任务元数据 | 33K | **20ms** | 30ms | 80ms |
| 原始日志行 | 19K | **110ms** | 780ms | 18.1s |

任务元数据查询中位数 20ms 返回。原始日志查询，中位数扫描一百万行，110ms 返回。

延迟与扫描行数大致成线性关系：

| 扫描行数 | 查询数 | 中位数延迟 | P95 延迟 |
|----------|--------|------------|----------|
| < 1K | 1,621 | 10ms | 50ms |
| 1K-10K | 2,608 | 20ms | 50ms |
| 10K-100K | 27,044 | 20ms | 50ms |
| 100K-1M | 8,515 | 40ms | 390ms |
| 1M-10M | 7,199 | 90ms | 1.2s |
| 10M-100M | 2,630 | 690ms | 6.8s |
| 100M-1B | 1,814 | 6.8s | 30.6s |
| 1B+ | 1,029 | 31s | 82s |

10 倍行数 ≈ 10 倍延迟。60% 的所有查询扫描少于 10 万行并在 50ms 内返回，足够快让 Agent 每秒发出几个而不会影响速度。在极端情况下，Agent 偶尔在单次查询中扫描超过 10 亿行；即使这些在中位数上也约 30 秒完成。

## 在 GitHub 速率限制下摄取数据

没有新鲜数据，以上都无法工作。Agent 需要推理刚刚失败的构建，而不是一小时前的。

### 速率限制约束

GitHub 的 API 为每个 App 安装每小时提供 15,000 次请求（非企业版计划为 5,000 次）。这听起来很慷慨，直到你需要在数十个活跃仓库中持续轮询工作流运行、任务、步骤和日志输出。单次提交可能产生数百个并行任务，每个都有需要获取的日志。

而且摄取不是唯一消耗 API 的。当 Agent 调查失败时，它会拉取 PR 元数据、读取文件差异、发布评论和打开 Pull Request。所有这些都计入相同的 15,000 请求配额。**限制摄取太激进，你的数据就会过时。限制太少，你会让 Agent 缺乏完成工作所需的 API 访问。**

早期，我们遇到了这个问题。我们的摄取会猛烈撞击速率限制，被阻塞剩余小时，然后落后。等它追上时，我们在摄取 30 多分钟前的日志。对于需要推理刚刚失败构建的 Agent 来说，这没用。如果工程师必须等待 Agent 跟上，他们已经切换上下文去手动调查了。

解决方案是节流：将请求均匀分布在速率限制窗口中，而不是突发。我们将摄取限制在大约每秒 3 个请求，为 Agent 每小时保留约 4,000 个请求。

一旦我们信任了节流机制，就将摄取速率提高了约 20%。更改后配额消耗更激进。我们在每个窗口中消耗更多可用余量，同时仍不完全耗尽。数据更新鲜，余量可接受。

我们的目标是摄取延迟 **P95 低于 5 分钟**，即 GitHub 上事件发生到在我们系统中可查询之间的时间。大多数时候，我们只需要几秒钟。

### 持久化执行（Durable execution）

我们的摄取管道和 Agent 都运行在 Inngest 上，一个持久化执行引擎。当任何一个遇到速率限制时，它不会崩溃、盲目重试或空转循环。它会**挂起（suspend）**。

GitHub 的速率限制响应头准确告诉你需要等待多久。我们读取该值，添加 10% 的抖动以避免限制重置时的惊群效应，然后挂起执行。完整状态被检查点保存：工作流进度、已获取的任务、日志分页位置。

等待结束后，执行在离开的精确位置恢复。无需重新初始化，无需重复工作。它继续下一个 API 调用，就像什么都没发生一样。

与替代方案比较：重试逻辑、状态恢复、去重。每个函数都需要幂等。每个中断的批次都需要协调。有了持久化执行，速率限制只是一个暂停按钮。

### 吸收流量峰值

CI 活动是突发的。有人合并大 PR，发布分支被切出，三个团队同时推送。我们的函数吞吐量：

队列工作在 CI 活动爆发期间激增至 3,000+。执行引擎吸收峰值并以稳定速率处理工作。

峰值活动期间出现峰值，但系统恢复。5 分钟 P95 目标保持不变：突发将延迟短暂推高，一旦队列排空就回落到秒级。

没人会在落地页上写"我们构建了一个非常好的速率限制器"。但没有新鲜、可查询的数据，你的 Agent 无法回答真正重要的问题：是我搞坏的，还是它本来就坏了？

---

*我们正在构建 Mendral（YC W26）。我们在 Docker 和 Dagger 花了十年时间构建和扩展 CI 系统，工作总是相同的：盯着日志、关联失败、找出变化。现在我们正在将其自动化。*
