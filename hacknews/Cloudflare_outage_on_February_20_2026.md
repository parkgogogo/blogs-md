URL: https://blog.cloudflare.com/cloudflare-outage-february-20-2026/

## Cloudflare outage on February 20, 2026

2026 年 2 月 20 日 Cloudflare 中断

On February 20, 2026, at 17:48 UTC, Cloudflare experienced a service outage when a subset of customers who use Cloudflare's Bring Your Own IP (BYOIP) service saw their routes to the Internet withdrawn via Border Gateway Protocol (BGP).

2026 年 2 月 20 日 17:48 UTC，Cloudflare 经历了一次服务中断，当时一部分使用 Cloudflare Bring Your Own IP (BYOIP) 服务的客户看到他们的互联网路由通过边界网关协议 (BGP) 被撤回。

The issue was not caused, directly or indirectly, by a cyberattack or malicious activity of any kind. This issue was caused by a change that Cloudflare made to how our network manages IP addresses onboarded through the BYOIP pipeline. This change caused Cloudflare to unintentionally withdraw customer prefixes.

这个问题不是由任何形式的网络攻击或恶意活动直接或间接引起的。这个问题是由 Cloudflare 对我们的网络管理通过 BYOIP 管道接入的 IP 地址的方式所做的更改引起的。这个更改导致 Cloudflare 无意中撤回了客户前缀。

For some BYOIP customers, this resulted in their services and applications being unreachable from the Internet, causing timeouts and failures to connect across their Cloudflare deployments that used BYOIP. The website for Cloudflare's recursive DNS resolver (1.1.1.1) saw 403 errors as well. The total duration of the incident was 6 hours and 7 minutes with most of that time spent restoring prefix configurations to their state prior to the change.

对于一些 BYOIP 客户，这导致他们的服务和应用程序无法从互联网访问，导致他们使用 BYOIP 的 Cloudflare 部署中出现超时和连接失败。Cloudflare 递归 DNS 解析器 (1.1.1.1) 的网站也出现了 403 错误。事件的总持续时间为 6 小时 7 分钟，其中大部分时间用于将前缀配置恢复到更改前的状态。

We are sorry for the impact to our customers. We let you down today. This post is an in-depth recounting of exactly what happened and which systems and processes failed. We will also outline the steps we are taking to prevent outages like this from happening again.

我们对给客户造成的影响感到抱歉。我们今天让您失望了。这篇文章详细记录了究竟发生了什么，以及哪些系统和流程失败了。我们还将概述我们正在采取的步骤，以防止类似的中断再次发生。

## How did the outage impact customers?

中断如何影响客户？

This graph shows the amount of prefixes advertised by Cloudflare during the incident to a BGP neighbor, which correlates to impact as prefixes that weren't advertised were unreachable on the Internet:

这张图显示了 Cloudflare 在事件期间向 BGP 邻居宣告的前缀数量，这与影响相关，因为未宣告的前缀在互联网上无法访问：

Out of the total 6,500 prefixes advertised to this peer, 4,306 of those were BYOIP prefixes. These BYOIP prefixes are advertised to every peer and represent all the BYOIP prefixes we advertise globally.

在向这个对等方宣告的 6,500 个前缀中，有 4,306 个是 BYOIP 前缀。这些 BYOIP 前缀被宣告给每个对等方，代表我们在全球宣告的所有 BYOIP 前缀。

During the incident, 1,100 prefixes out of the total 6,500 were withdrawn from 17:56 to 18:46 UTC. Out of the 4,306 total BYOIP prefixes, 25% of BYOIP prefixes were unintentionally withdrawn.

在事件期间，从 17:56 到 18:46 UTC，总共 6,500 个前缀中有 1,100 个被撤回。在总共 4,306 个 BYOIP 前缀中，25% 的 BYOIP 前缀被无意中撤回。

## Timeline

时间线

All times are in UTC.

所有时间均为 UTC。

- 17:48 - Cloudflare implements a change in production to refactor elements of BYOIP prefix management.
- 17:48 - Cloudflare 在生产环境中实施了一项更改，以重构 BYOIP 前缀管理的某些元素。
- 17:54 - Automated systems detect that prefixes have been withdrawn and page the on-call engineer.
- 17:54 - 自动化系统检测到前缀已被撤回，并 paging 值班工程师。
- 17:56 - Customers begin reporting issues on social media and our community forum.
- 17:56 - 客户开始在社交媒体和我们的社区论坛上报告问题。
- 18:22 - The engineering team identifies the change as the likely cause and begins rollback.
- 18:22 - 工程团队确定该更改是可能的原因，并开始回滚。

---

**批判性思考评论：**

这是一份典型的 Cloudflare 事后分析文档——透明、详细、自责。但除了表面的事故描述，这篇文章揭示了几个深层问题：

1. **配置管理的复杂性**：BYOIP（Bring Your Own IP）服务允许客户使用自己的 IP 地址，这意味着 Cloudflare 需要在其全球网络中管理大量客户特定的 BGP 配置。这种复杂性是扩展性的代价。

2. **自动化检测的滞后**：自动化系统在 17:54 检测到前缀撤回（更改后 6 分钟），但客户早在 17:56 就开始报告问题。这表明自动化监控虽然有效，但仍有改进空间。

3. **回滚的挑战**：从发现问题到完成回滚用了近 4 小时，这暴露了大规模分布式系统中配置回滚的困难——特别是在 BGP 配置已经传播到全球的情况下。

4. **平台风险集中化**：Cloudflare 作为互联网基础设施的关键节点，其中断影响广泛。即使是"仅"25% 的 BYOIP 前缀受影响，也影响了 1,100 个前缀。这提醒我们互联网中心化带来的系统性风险。
