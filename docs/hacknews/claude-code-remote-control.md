# Claude Code Remote Control
# Claude Code 远程控制

**Source:** https://code.claude.com/docs/en/remote-control  
**Date:** 2026-02-25

Anthropic has announced Remote Control capabilities for Claude Code, enabling developers to programmatically control and extend the AI coding assistant's functionality. This new feature opens up possibilities for automated workflows and custom integrations.

Anthropic 宣布了 Claude Code 的远程控制功能，使开发者能够以编程方式控制和扩展 AI 编程助手的功能。这一新功能为自动化工作流和自定义集成开辟了可能性。

Remote Control allows external applications to send commands to Claude Code and receive structured responses, effectively turning the coding assistant into an API-accessible service. This enables integration with CI/CD pipelines, custom IDEs, and automated development tools.

远程控制允许外部应用向 Claude Code 发送命令并接收结构化响应，有效地将编程助手转变为可通过 API 访问的服务。这使得与 CI/CD 管道、自定义 IDE 和自动化开发工具的集成成为可能。

Key capabilities:
- Programmatic file editing and navigation
- Automated code review and refactoring
- Integration with testing and deployment workflows
- Custom command creation and execution

主要能力：
- 程序化文件编辑和导航
- 自动化代码审查和重构
- 与测试和部署工作流集成
- 自定义命令创建和执行

The feature is designed with security in mind, requiring explicit user authorization for remote connections and maintaining audit logs of all actions. Users can define fine-grained permissions controlling what remote clients can access.

该功能在设计时考虑了安全性，需要用户对远程连接进行明确授权，并维护所有操作的审计日志。用户可以定义细粒度的权限，控制远程客户端可以访问的内容。

Anthropic provides SDKs for popular languages including Python, TypeScript, and Go, making it straightforward to build applications that interact with Claude Code. The protocol uses standard web technologies for broad compatibility.

Anthropic 为流行语言（包括 Python、TypeScript 和 Go）提供 SDK，使构建与 Claude Code 交互的应用变得简单。该协议使用标准 Web 技术以实现广泛的兼容性。

Use cases demonstrated by early adopters include automated code migration, intelligent documentation generation, and AI-powered code review bots that integrate with GitHub workflows.

早期采用者展示的用例包括自动代码迁移、智能文档生成和与 GitHub 工作流集成的 AI 驱动代码审查机器人。

The Remote Control API is available to all Claude Code subscribers and represents a significant step toward Claude becoming a platform rather than just a standalone tool.

远程控制 API 可供所有 Claude Code 订阅者使用，代表着 Claude 向成为平台而不仅仅是独立工具迈出的重要一步。
