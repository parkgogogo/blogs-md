# 停止浪费你的上下文窗口——我们构建了上下文模式

**Original:** https://mksg.lu/blog/context-mode  
**Rating:** 9/10 | **Category:** AI

---

## English Content

Context Mode is an MCP server that reduces Claude Code context consumption by 98%. 

The article explains:
- Sandbox architecture with isolated subprocesses
- SQLite FTS5 knowledge base with BM25 ranking
- Practical implementation details
- How proper tool design extends AI coding sessions from 30 minutes to 3 hours

Key insights:
- Traditional MCP tools consume excessive context window
- Context Mode uses a sandboxed approach to minimize token usage
- SQLite with FTS5 enables efficient knowledge retrieval
- BM25 ranking provides relevant context without overwhelming the model

---

## 中文翻译

Context Mode 是一个 MCP 服务器，可将 Claude Code 的上下文消耗减少 98%。

文章解释了：
- 具有隔离子进程的沙盒架构
- 带有 BM25 排名的 SQLite FTS5 知识库
- 实际实现细节
- 适当的工具设计如何将 AI 编程会话从 30 分钟延长到 3 小时

关键见解：
- 传统 MCP 工具消耗过多的上下文窗口
- Context Mode 使用沙盒方法来最小化令牌使用
- 带有 FTS5 的 SQLite 实现高效的知识检索
- BM25 排名提供相关上下文而不会压垮模型
