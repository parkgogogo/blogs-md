URL: https://kevinak.se/blog/be-wary-of-bluesky

## Be Wary of Bluesky

警惕 Bluesky

In 2023, Bluesky's CTO Paul Frazee was asked what would happen if Bluesky ever turned against its users. His answer:

2023 年，Bluesky 的 CTO Paul Frazee 被问到如果 Bluesky 有一天背叛其用户会发生什么。他的回答是：

"it would look something like this: bluesky has gone evil. there's a new alternative called freesky that people are rushing to. I'm switching to freesky"

"情况会是这样的：bluesky 变邪恶了。有一个叫 freesky 的新替代品，人们正在涌向它。我要转向 freesky"

That's the same argument people made about Twitter. "If it goes bad, we'll just leave." We know how that played out.

这与人们对 Twitter 的论点相同。"如果它变糟了，我们就离开。"我们知道结果如何。

## The promise

承诺

Bluesky is built on ATProto, an open protocol. The pitch is simple: your data is yours, your identity is yours, and if you don't like what Bluesky is doing, you can take everything and leave. Apps like Tangled (git hosting), Grain (photos), and Leaflet (publishing) all plug into the same protocol. One account, many apps, no lock-in.

Bluesky 建立在 ATProto 之上，这是一个开放协议。宣传很简单：你的数据是你的，你的身份是你的，如果你不喜欢 Bluesky 正在做的事情，你可以带着一切离开。像 Tangled（git 托管）、Grain（照片）和 Leaflet（出版）这样的应用都接入同一个协议。一个账户，多个应用，没有锁定。

It sounds great. But look closer.

听起来很棒。但仔细看。

## Where your data actually lives

你的数据实际存储在哪里

When you use any ATProto app, it writes data to your Personal Data Server, or PDS. Your Bluesky posts, your Tangled issues, your Leaflet publications, your Grain photos. All of it goes to the same place.

当你使用任何 ATProto 应用时，它会将数据写入你的个人数据服务器（PDS）。你的 Bluesky 帖子、你的 Tangled 议题、你的 Leaflet 出版物、你的 Grain 照片。所有这些都去往同一个地方。

For almost every user, that place is a server run by Bluesky.

对于几乎每个用户来说，那个地方就是 Bluesky 运行的服务器。

You can self-host a PDS. Almost nobody does. Why would they? Bluesky's PDS works out of the box with every app, zero setup, zero maintenance. Self-hosting means running a server, keeping it online, and gaining nothing in return.

你可以自己托管 PDS。几乎没有人这样做。为什么要呢？Bluesky 的 PDS 与每个应用开箱即用，零设置，零维护。自己托管意味着运行服务器，保持在线，却得不到任何回报。

## The flywheel

飞轮效应

Here's the part that worries me.

这是让我担心的部分。

Every new ATProto app makes this problem worse, not better. Each app tells you "sign in with your Bluesky account", which really means "write more data to Bluesky's servers." The more apps that launch, the more users depend on Bluesky's infrastructure, the less reason anyone has to leave.

每个新的 ATProto 应用都让这个问题变得更糟，而不是更好。每个应用都告诉你"用你的 Bluesky 账户登录"，这实际上意味着"向 Bluesky 的服务器写入更多数据。"启动的应用越多，用户越依赖 Bluesky 的基础设施，任何人离开的理由就越少。

The protocol doesn't distribute value across the network. It concentrates it. Developers are building features on top of Bluesky's infrastructure for free, making it more indispensable with every app that ships.

协议并没有在整个网络中分配价值。它集中了价值。开发者正在免费在 Bluesky 的基础设施之上构建功能，让每个发布的应用都让它变得更加不可或缺。

## The chokepoints

扼制点

It's not just the PDS. Bluesky controls almost every critical layer:

不仅仅是 PDS。Bluesky 控制着几乎每个关键层：

The Relay. All data flows through it. Bluesky runs the dominant one. Whoever controls the relay controls what gets seen, hidden, or deprioritized. Third parties can run their own, but without the users, it doesn't matter.

中继（Relay）。所有数据都通过它流动。Bluesky 运行着主导的中继。谁控制中继，谁就控制什么被看到、隐藏或降权。第三方可以运行自己的中继，但没有用户，这无关紧要。

The AppView. This is what assembles your timeline, threads, and notifications. Bluesky runs the main one. If it goes down or goes hostile, every client that depends on it breaks.

应用视图（AppView）。这是组装你的时间线、帖子和通知的东西。Bluesky 运行着主要的应用视图。如果它宕机或变得敌对，每个依赖它的客户端都会崩溃。

---

**批判性思考评论：**

这篇文章对 Bluesky 的批评切中要害，揭示了一个常被忽视的真相：开放协议并不自动意味着去中心化或用户主权。

关键论点：

1. **形式上的开放 vs 实质上的集中**：ATProto 是开放协议，但绝大多数用户的数据存储在 Bluesky 运行的 PDS 上。这和 Gmail 与电子邮件的关系类似——任何人都可以运行邮件服务器，但实践中大家都用 Gmail。

2. **飞轮效应的陷阱**：每个新 ATProto 应用实际上都增加了对 Bluesky 基础设施的依赖，而非减少。这与传统联邦制协议（如电子邮件）不同，在电子邮件中每个应用连接的是用户自己的服务器。

3. **多点扼制**：PDS、Relay、AppView、DID Directory——理论上每个都可以独立运行，但实践中 Bluesky 控制着所有这些层的默认实例。这种架构使得"退出"在技术上可能但在实践中困难。

4. **收购风险**：如果 Bluesky 被收购，收购方将控制：几乎所有用户的 PDS、主要中继、主要 AppView、解析每个身份的 DID 目录。他们可以禁用数据导出、切断第三方应用、插入广告——而用户的迁移成本会随着时间推移越来越高。

这篇文章提醒我们：在评估"去中心化"项目时，我们需要关注实际的数据流动和基础设施控制，而不仅仅是协议规范。
