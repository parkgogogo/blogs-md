URL: https://blog.cloudflare.com/vinext/

# How we rebuilt Next.js with AI in one week
# 我们如何在一周内用AI重建Next.js

---

*This post was updated at 12:35 pm PT to fix a typo in the build time benchmarks.*

*本文已于太平洋时间12:35更新，以修复构建时间基准测试中的一个拼写错误。*

---

Last week, one engineer and an AI model rebuilt the most popular front-end framework from scratch. The result, [vinext](https://github.com/cloudflare/vinext) (pronounced "vee-next"), is a drop-in replacement for Next.js, built on [Vite](https://vite.dev/), that deploys to Cloudflare Workers with a single command. In early benchmarks, it builds production apps up to 4x faster and produces client bundles up to 57% smaller. And we already have customers running it in production.

上周，一名工程师和一个AI模型从头重建了最流行的前端框架。结果产物是 [vinext](https://github.com/cloudflare/vinext)（发音为"vee-next"），这是一个基于 [Vite](https://vite.dev/) 的Next.js即插即用替代品，只需一个命令即可部署到Cloudflare Workers。在早期基准测试中，它的生产应用构建速度提高了4倍，客户端包体积缩小了57%。而且我们已经有客户在将其实际用于生产环境。

---

The whole thing cost about $1,100 in tokens.

整个项目的token成本约为1100美元。

---

## The Next.js deployment problem
## Next.js的部署难题

---

[Next.js](https://nextjs.org/) is the most popular React framework. Millions of developers use it. It powers a huge chunk of the production web, and for good reason. The developer experience is top-notch.

[Next.js](https://nextjs.org/) 是最流行的React框架。数百万开发者使用它。它为大量生产级网站提供支持，这是有原因的。开发者体验是一流的。

---

But Next.js has a deployment problem when used in the broader serverless ecosystem. The tooling is entirely bespoke: Next.js has invested heavily in Turbopack but if you want to deploy it to Cloudflare, Netlify, or AWS Lambda, you have to take that build output and reshape it into something the target platform can actually run.

但当Next.js用于更广泛的无服务器生态系统时，它存在一个部署问题。其工具链完全是定制的：Next.js在Turbopack上投入了大量资源，但如果你想将其部署到Cloudflare、Netlify或AWS Lambda，你必须获取构建输出并将其重塑为目标平台实际可运行的东西。

---

If you're thinking: "Isn't that what OpenNext does?", you are correct.

如果你在想："这不是OpenNext做的事情吗？"，你是对的。

---

That is indeed the problem [OpenNext](https://opennext.js.org/) was built to solve. And a lot of engineering effort has gone into OpenNext from multiple providers, including us at Cloudflare. It works, but quickly runs into limitations and becomes a game of whack-a-mole.

这确实是 [OpenNext](https://opennext.js.org/) 旨在解决的问题。多个提供商（包括我们Cloudflare）为OpenNext投入了大量的工程工作。它能用，但很快就会遇到限制，变成一场打地鼠游戏。

---

Building on top of Next.js output as a foundation has proven to be a difficult and fragile approach. Because OpenNext has to reverse-engineer Next.js's build output, this results in unpredictable changes between versions that take a lot of work to correct.

事实证明，以Next.js输出作为基础进行构建是一种困难且脆弱的方法。因为OpenNext必须逆向工程Next.js的构建输出，这导致版本之间出现不可预测的变化，需要大量工作来修正。

---

Next.js has been working on a first-class adapters API, and we've been collaborating with them on it. It's still an early effort but even with adapters, you're still building on the bespoke Turbopack toolchain. And adapters only cover build and deploy. During development, next dev runs exclusively in Node.js with no way to plug in a different runtime. If your application uses platform-specific APIs like Durable Objects, KV, or AI bindings, you can't test that code in dev without workarounds.

Next.js一直在开发一流的适配器API，我们一直在与他们合作。这仍然是一个早期工作，但即使有适配器，你仍然在基于定制的Turbopack工具链进行构建。而且适配器只涵盖构建和部署。在开发过程中，next dev仅在Node.js中运行，无法插入不同的运行时。如果你的应用程序使用平台特定的API，如Durable Objects、KV或AI绑定，你无法在开发中测试这些代码而不需要变通方法。

---

## Introducing vinext
## 介绍vinext

---

What if instead of adapting Next.js output, we reimplemented the Next.js API surface on [Vite](https://vite.dev/) directly? Vite is the build tool used by most of the front-end ecosystem outside of Next.js, powering frameworks like Astro, SvelteKit, Nuxt, and Remix. A clean reimplementation, not merely a wrapper or adapter. We honestly didn't think it would work. But it's 2026, and the cost of building software has completely changed.

如果我们可以直接在 [Vite](https://vite.dev/) 上重新实现Next.js API表面，而不是适配Next.js输出，会怎样？Vite是Next.js之外大多数前端生态系统使用的构建工具，为Astro、SvelteKit、Nuxt和Remix等框架提供支持。这是一次干净的重新实现，不仅仅是包装器或适配器。老实说，我们并不认为这能成功。但现在是2026年，构建软件的成本已经完全改变了。

---

We got a lot further than we expected.

我们取得的进展远超预期。

---

```typescript
npm install vinext
```

---

Replace `next` with `vinext` in your scripts and everything else stays the same. Your existing `app/`, `pages/`, and `next.config.js` work as-is.

在脚本中将 `next` 替换为 `vinext`，其他一切保持不变。你现有的 `app/`、`pages/` 和 `next.config.js` 可以原样工作。

---

```shell
vinext dev          # Development server with HMR
vinext build        # Production build
vinext deploy       # Build and deploy to Cloudflare Workers
```

```shell
vinext dev          # 带HMR的开发服务器
vinext build        # 生产构建
vinext deploy       # 构建并部署到Cloudflare Workers
```

---

This is not a wrapper around Next.js and Turbopack output. It's an alternative implementation of the API surface: routing, server rendering, React Server Components, server actions, caching, middleware. All of it built on top of Vite as a plugin. Most importantly Vite output runs on any platform thanks to the [Vite Environment API](https://vite.dev/guide/api-environment).

这不是围绕Next.js和Turbopack输出的包装器。这是API表面的替代实现：路由、服务器渲染、React服务器组件、服务器操作、缓存、中间件。所有这些都作为插件构建在Vite之上。最重要的是，由于 [Vite环境API](https://vite.dev/guide/api-environment)，Vite输出可以在任何平台上运行。

---

## The numbers
## 数据表现

---

Early benchmarks are promising. We compared vinext against Next.js 16 using a shared 33-route App Router application.

早期基准测试很有希望。我们使用一个共享的33路由App Router应用程序将vinext与Next.js 16进行了比较。

---

Both frameworks are doing the same work: compiling, bundling, and preparing server-rendered routes. We disabled TypeScript type checking and ESLint in Next.js's build (Vite doesn't run these during builds), and used force-dynamic so Next.js doesn't spend extra time pre-rendering static routes, which would unfairly slow down its numbers. The goal was to measure only bundler and compilation speed, nothing else. Benchmarks run on GitHub CI on every merge to main.

两个框架都在做同样的工作：编译、打包和准备服务器渲染路由。我们在Next.js构建中禁用了TypeScript类型检查和ESLint（Vite在构建期间不运行这些），并使用force-dynamic，这样Next.js就不会花费额外时间预渲染静态路由，这会不公平地降低其数据。目标只是衡量打包器和编译速度，其他什么都不测。基准测试在每次合并到main时在GitHub CI上运行。

---

**Production build time:**

**生产构建时间：**

| Framework | Mean | vs Next.js |
|-----------|------|------------|
| Next.js 16.1.6 (Turbopack) | 7.38s | baseline |
| vinext (Vite 7 / Rollup) | 4.64s | 1.6x faster |
| vinext (Vite 8 / Rolldown) | 1.67s | 4.4x faster |

| 框架 | 平均值 | 对比Next.js |
|-----------|------|------------|
| Next.js 16.1.6 (Turbopack) | 7.38秒 | 基准线 |
| vinext (Vite 7 / Rollup) | 4.64秒 | 快1.6倍 |
| vinext (Vite 8 / Rolldown) | 1.67秒 | 快4.4倍 |

---

**Client bundle size (gzipped):**

**客户端包大小（gzip压缩后）：**

| Framework | Gzipped | vs Next.js |
|-----------|---------|------------|
| Next.js 16.1.6 | 168.9 KB | baseline |
| vinext (Rollup) | 74.0 KB | 56% smaller |
| vinext (Rolldown) | 72.9 KB | 57% smaller |

| 框架 | Gzip压缩后 | 对比Next.js |
|-----------|---------|------------|
| Next.js 16.1.6 | 168.9 KB | 基准线 |
| vinext (Rollup) | 74.0 KB | 小56% |
| vinext (Rolldown) | 72.9 KB | 小57% |

---

These benchmarks measure compilation and bundling speed, not production serving performance. The test fixture is a single 33-route app, not a representative sample of all production applications. We expect these numbers to evolve as three projects continue to develop. The [full methodology and historical results](https://benchmarks.vinext.workers.dev) are public. Take them as directional, not definitive.

这些基准测试衡量编译和打包速度，而不是生产服务性能。测试装置是一个单一的33路由应用程序，不是所有生产应用程序的代表性样本。随着三个项目的继续发展，我们预计这些数字会发生变化。[完整的方法和历史结果](https://benchmarks.vinext.workers.dev)是公开的。将它们作为方向性的，而非确定性的。

---

The direction is encouraging, though. Vite's architecture, and especially [Rolldown](https://rolldown.rs/) (the Rust-based bundler coming in Vite 8), has structural advantages for build performance that show up clearly here.

不过，这个方向令人鼓舞。Vite的架构，特别是 [Rolldown](https://rolldown.rs/)（即将在Vite 8中推出的基于Rust的打包器），在构建性能方面具有结构优势，在这里表现得很明显。

---

## Deploying to Cloudflare Workers
## 部署到Cloudflare Workers

---

vinext is built with Cloudflare Workers as the first deployment target. A single command takes you from source code to a running Worker:

vinext以Cloudflare Workers作为首个部署目标构建。一个命令即可将源代码转换为正在运行的Worker：

---

```shell
vinext deploy
```

---

This handles everything: builds the application, auto-generates the Worker configuration, and deploys. Both the App Router and Pages Router work on Workers, with full client-side hydration, interactive components, client-side navigation, React state.

这处理了一切：构建应用程序、自动生成Worker配置并部署。App Router和Pages Router都可以在Workers上运行，具有完整的客户端hydration、交互式组件、客户端导航、React状态。

---

For production caching, vinext includes a Cloudflare KV cache handler that gives you ISR (Incremental Static Regeneration) out of the box:

对于生产缓存，vinext包含一个Cloudflare KV缓存处理程序，可立即为你提供ISR（增量静态再生）：

---

```typescript
import { KVCacheHandler } from "vinext/cloudflare";
import { setCacheHandler } from "next/cache";

setCacheHandler(new KVCacheHandler(env.MY_KV_NAMESPACE));
```

---

[KV](https://developers.cloudflare.com/kv/) is a good default for most applications, but the caching layer is designed to be pluggable. That setCacheHandler call means you can swap in whatever backend makes sense. [R2](https://developers.cloudflare.com/r2/) might be a better fit for apps with large cached payloads or different access patterns. We're also working on improvements to our Cache API that should provide a strong caching layer with less configuration. The goal is flexibility: pick the caching strategy that fits your app.

[KV](https://developers.cloudflare.com/kv/) 是大多数应用程序的良好默认选择，但缓存层设计为可插拔的。setCacheHandler调用意味着你可以换成任何有意义的后端。[R2](https://developers.cloudflare.com/r2/) 可能更适合具有大缓存负载或不同访问模式的应用程序。我们还在改进我们的缓存API，以提供更强大的缓存层和更少的配置。目标是灵活性：选择适合你应用程序的缓存策略。

---

Live examples running right now:

目前正在运行的实时示例：

- [App Router Playground](https://app-router-playground.vinext.workers.dev)
- [Hacker News clone](https://hackernews.vinext.workers.dev)
- [App Router minimal](https://app-router-cloudflare.vinext.workers.dev)
- [Pages Router minimal](https://pages-router-cloudflare.vinext.workers.dev)

---

We also have [a live example](https://next-agents.threepointone.workers.dev/) of Cloudflare Agents running in a Next.js app, without the need for workarounds like [getPlatformProxy](https://developers.cloudflare.com/workers/wrangler/api/#getplatformproxy), since the entire app now runs in workerd, during both dev and deploy phases. This means being able to use Durable Objects, AI bindings, and every other Cloudflare-specific service without compromise. [Have a look here.](https://github.com/cloudflare/vinext-agents-example)

我们还有一个在Next.js应用程序中运行Cloudflare Agents的 [实时示例](https://next-agents.threepointone.workers.dev/)，不需要像 [getPlatformProxy](https://developers.cloudflare.com/workers/wrangler/api/#getplatformproxy) 这样的变通方法，因为整个应用程序现在在开发和部署阶段都在workerd中运行。这意味着能够毫无妥协地使用Durable Objects、AI绑定和所有其他Cloudflare特定的服务。[在这里查看。](https://github.com/cloudflare/vinext-agents-example)

---

## Frameworks are a team sport
## 框架是团队运动

---

The current deployment target is Cloudflare Workers, but that's a small part of the picture. Something like 95% of vinext is pure Vite. The routing, the module shims, the SSR pipeline, the RSC integration: none of it is Cloudflare-specific.

当前的部署目标是Cloudflare Workers，但这只是整个图景的一小部分。vinext大约95%是纯Vite。路由、模块shim、SSR管道、RSC集成：没有一个是Cloudflare特有的。

---

Cloudflare is looking to work with other hosting providers about adopting this toolchain for their customers (the lift is minimal — we got a proof-of-concept working on [Vercel](https://vinext-on-vercel.vercel.app/) in less than 30 minutes!). This is an open-source project, and for its long term success, we believe it's important we work with partners across the ecosystem to ensure ongoing investment. PRs from other platforms are welcome. If you're interested in adding a deployment target, [open an issue](https://github.com/cloudflare/vinext/issues) or reach out.

Cloudflare正在寻求与其他托管提供商合作，为他们的客户采用这个工具链（工作量很小——我们在不到30分钟内在 [Vercel](https://vinext-on-vercel.vercel.app/) 上完成了概念验证！）。这是一个开源项目，为了它的长期成功，我们相信与生态系统中的合作伙伴合作以确保持续投入是很重要的。欢迎来自其他平台的PR。如果你有兴趣添加部署目标，请[提交issue](https://github.com/cloudflare/vinext/issues)或联系我们。

---

## Status: Experimental
## 状态：实验性

---

We want to be clear: vinext is experimental. It's not even one week old, and it has not yet been battle-tested with any meaningful traffic at scale. If you're evaluating it for a production application, proceed with appropriate caution.

我们要明确：vinext是实验性的。它还不到一周，尚未经过任何有意义的规模流量实战测试。如果你正在评估将其用于生产应用程序，请谨慎行事。

---

That said, the test suite is extensive: over 1,700 Vitest tests and 380 Playwright E2E tests, including tests ported directly from the Next.js test suite and OpenNext's Cloudflare conformance suite. We've verified it against the Next.js App Router Playground. Coverage sits at 94% of the Next.js 16 API surface.

也就是说，测试套件非常广泛：超过1,700个Vitest测试和380个Playwright E2E测试，包括直接从Next.js测试套件和OpenNext的Cloudflare一致性套件移植的测试。我们已经针对Next.js App Router Playground进行了验证。覆盖率达到了Next.js 16 API表面的94%。

---

Early results from real-world customers are encouraging. We've been working with [National Design Studio](https://ndstudio.gov/), a team that's aiming to modernize every government interface, on one of their beta sites, [CIO.gov](https://www.cio.gov/). They're already running vinext in production, with meaningful improvements in build times and bundle sizes.

来自真实客户的早期结果令人鼓舞。我们一直在与 [National Design Studio](https://ndndstudio.gov/) 合作，这是一个旨在现代化每个政府界面的团队，在他们的一个测试站点 [CIO.gov](https://www.cio.gov/) 上。他们已经在生产环境中运行vinext，构建时间和包大小都有显著改善。

---

The README is honest about [what's not supported and won't be](https://github.com/cloudflare/vinext#whats-not-supported-and-wont-be), and about [known limitations](https://github.com/cloudflare/vinext#known-limitations). We want to be upfront rather than overpromise.

README坦诚说明了 [不支持且不会支持的内容](https://github.com/cloudflare/vinext#whats-not-supported-and-wont-be)，以及 [已知的限制](https://github.com/cloudflare/vinext#known-limitations)。我们宁愿坦诚也不愿过度承诺。

---

## What about pre-rendering?
## 那预渲染呢？

---

vinext already supports Incremental Static Regeneration (ISR) out of the box. After the first request to any page, it's cached and revalidated in the background, just like Next.js. That part works today.

vinext已经原生支持增量静态再生（ISR）。在对任何页面发出第一个请求后，它会被缓存并在后台重新验证，就像Next.js一样。这部分今天已经可以工作。

---

vinext does not yet support static pre-rendering at build time. In Next.js, pages without dynamic data get rendered during `next build` and served as static HTML. If you have dynamic routes, you use `generateStaticParams()` to enumerate which pages to build ahead of time. vinext doesn't do that… yet.

vinext尚不支持构建时的静态预渲染。在Next.js中，没有动态数据的页面会在 `next build` 期间渲染并作为静态HTML提供服务。如果你有动态路由，可以使用 `generateStaticParams()` 来枚举要提前构建哪些页面。vinext还没有这样做……还没有。

---

This was an intentional design decision for launch. It's [on the roadmap](https://github.com/cloudflare/vinext/issues/9), but if your site is 100% prebuilt HTML with static content, you probably won't see much benefit from vinext today. That said, if one engineer can spend $1,100 in tokens and rebuild Next.js, you can probably spend $10 and migrate to a Vite-based framework designed specifically for static content, like [Astro](https://astro.build/) (which [also deploys to Cloudflare Workers](https://blog.cloudflare.com/astro-joins-cloudflare/)).

这是发布时有意为之的设计决定。它 [在路线图上](https://github.com/cloudflare/vinext/issues/9)，但如果你的网站是100%预构建的静态内容HTML，你今天可能不会从vinext中看到太多好处。也就是说，如果一名工程师可以花费1100美元的token重建Next.js，你可能可以花10美元迁移到专门为静态内容设计的基于Vite的框架，如 [Astro](https://astro.build/)（它 [也部署到Cloudflare Workers](https://blog.cloudflare.com/astro-joins-cloudflare/)）。

---

For sites that aren't purely static, though, we think we can do something better than pre-rendering everything at build time.

不过，对于不完全静态的网站，我们认为我们可以做一些比在构建时预渲染所有内容更好的事情。

---

## Introducing Traffic-aware Pre-Rendering
## 介绍流量感知预渲染

---

Next.js pre-renders every page listed in `generateStaticParams()` during the build. A site with 10,000 product pages means 10,000 renders at build time, even though 99% of those pages may never receive a request. Builds scale linearly with page count. This is why large Next.js sites end up with 30-minute builds.

Next.js在构建期间预渲染 `generateStaticParams()` 中列出的每个页面。一个有10,000个产品页面的网站意味着构建时有10,000次渲染，即使其中99%的页面可能永远不会收到请求。构建时间与页面数量成线性比例。这就是大型Next.js网站最终需要30分钟构建时间的原因。

---

So we built **Traffic-aware Pre-Rendering** (TPR). It's experimental today, and we plan to make it the default once we have more real-world testing behind it.

因此我们构建了 **流量感知预渲染**（TPR）。它今天是实验性的，一旦我们有了更多真实世界的测试，我们计划将其设为默认。

---

The idea is simple. Cloudflare is already the reverse proxy for your site. We have your traffic数据。我们知道哪些页面实际被访问过。因此，vinext不是预渲染所有内容或不预渲染任何内容，而是在部署时查询Cloudflare的区域分析数据，只预渲染那些重要的页面。

The idea is simple. Cloudflare is already the reverse proxy for your site. We have your traffic data. We know which pages actually get visited. So instead of pre-rendering everything or pre-rendering nothing, vinext queries Cloudflare's zone analytics at deploy time and pre-renders only the pages that matter.

---

```javascript
vinext deploy --experimental-tpr

  Building...
  Build complete (4.2s)

  TPR (experimental): Analyzing traffic for my-store.com (last 24h)
  TPR: 12,847 unique paths — 184 pages cover 90% of traffic
  TPR: Pre-rendering 184 pages...
  TPR: Pre-rendered 184 pages in 8.3s → KV cache

  Deploying to Cloudflare Workers...
```

---

For a site with 100,000 product pages, the power law means 90% of traffic usually goes to 50 to 200 pages. Those get pre-rendered in seconds. Everything else falls back to on-demand SSR and gets cached via ISR after the first request. Every new deploy refreshes the set based on current traffic patterns. Pages that go viral get picked up automatically. All of this works without `generateStaticParams()` and without coupling your build to your production database.

对于一个有100,000个产品页面的网站，幂律意味着90%的流量通常流向50到200个页面。这些页面在几秒钟内就能预渲染完成。其他所有内容都回退到按需SSR，并在第一次请求后通过ISR缓存。每次新部署都会根据当前流量模式刷新集合。 viral的页面会自动被捕获。所有这些都不需要 `generateStaticParams()`，也不需要将你的构建与生产数据库耦合。

---

## Taking on the Next.js challenge, but this time with AI
## 接受Next.js挑战，但这次用AI

---

A project like this would normally take a team of engineers months, if not years. Several teams at various companies have attempted it, and the scope is just enormous. We tried once at Cloudflare! Two routers, 33+ module shims, server rendering pipelines, RSC streaming, file-system routing, middleware, caching, static export. There's a reason nobody has pulled it off.

像这样的项目通常需要一支工程师团队花费数月甚至数年的时间。多家公司的几个团队都尝试过，范围实在太大了。我们在Cloudflare尝试过一次！两个路由器、33+模块shim、服务器渲染管道、RSC流、文件系统路由、中间件、缓存、静态导出。没有人成功是有原因的。

---

This time we did it in under a week. One engineer (technically engineering manager) directing AI.

这次我们在不到一周的时间内完成了。一名工程师（技术上讲是工程经理）指导AI。

---

The first commit landed on February 13. By the end of that same evening, both the Pages Router and App Router had basic SSR working, along with middleware, server actions, and streaming. By the next afternoon, [App Router Playground](https://app-router-playground.vinext.workers.dev) was rendering 10 of 11 routes. By day three, `vinext deploy` was shipping apps to Cloudflare Workers with full client hydration. The rest of the week was hardening: fixing edge cases, expanding the test suite, bringing API coverage to 94%.

第一次提交是在2月13日。到当天晚上结束时，Pages Router和App Router都具备了基本的SSR功能，以及中间件、服务器操作和流。到第二天下午，[App Router Playground](https://app-router-playground.vinext.workers.dev) 已经渲染了11个路由中的10个。到第三天，`vinext deploy` 正在将应用程序部署到Cloudflare Workers，并具有完整的客户端hydration。这周剩下的时间是加固：修复边缘情况、扩展测试套件、将API覆盖率提高到94%。

---

What changed from those earlier attempts? AI got better. Way better.

与早期尝试相比发生了什么变化？AI变得更好了。好多了。

---

## Why this problem is made for AI
## 为什么这个问题适合AI

---

Not every project would go this way. This one did because a few things happened to line up at the right time.

不是每个项目都会这样进行。这个项目之所以这样，是因为几件事情在正确的时间恰好对齐了。

---

**Next.js is well-specified.** It has extensive documentation, a massive user base, and years of Stack Overflow answers and tutorials. The API surface is all over the training data. When you ask Claude to implement `getServerSideProps` or explain how `useRouter` works, it doesn't hallucinate. It knows how Next works.

**Next.js定义良好。** 它有广泛的文档、庞大的用户群，以及多年的Stack Overflow答案和教程。API表面遍布训练数据。当你让Claude实现 `getServerSideProps` 或解释 `useRouter` 如何工作时，它不会产生幻觉。它知道Next是如何工作的。

---

**Next.js has an elaborate test suite.** The [Next.js repo](https://github.com/vercel/next.js) contains thousands of E2E tests covering every feature and edge case. We ported tests directly from their suite (you can see the attribution in the code). This gave us a specification we could verify against mechanically.

**Next.js有精心设计的测试套件。** [Next.js仓库](https://github.com/vercel/next.js) 包含数千个E2E测试，涵盖每个功能和边缘情况。我们直接从他们的套件移植了测试（你可以在代码中看到归属）。这给了我们一个可以机械验证的规范。

---

**Vite is an excellent foundation.** [Vite](https://vite.dev/) handles the hard parts of front-end tooling: fast HMR, native ESM, a clean plugin API, production bundling. We didn't have to build a bundler. We just had to teach it to speak Next.js. [`@vitejs/plugin-rsc`](https://github.com/vitejs/vite-plugin-rsc) is still early, but it gave us React Server Components support without having to build an RSC implementation from scratch.

**Vite是一个优秀的基础。** [Vite](https://vite.dev/) 处理前端工具的难点：快速HMR、原生ESM、干净的插件API、生产打包。我们不必构建打包器。我们只需要教会它说Next.js。 [`@vitejs/plugin-rsc`](https://github.com/vitejs/vite-plugin-rsc) 还处于早期阶段，但它给了我们React服务器组件支持，而不必从头构建RSC实现。

---

**The models caught up.** We don't think this would have been possible even a few months ago. Earlier models couldn't sustain coherence across a codebase this size. New models can hold the full architecture in context, reason about how modules interact, and produce correct code often enough to keep momentum going. At times, I saw it go into Next, Vite, and React internals to figure out a bug. The state-of-the-art models are impressive, and they seem to keep getting better.

**模型赶上了。** 我们认为即使几个月前这也是不可能的。早期的模型无法在这种规模的代码库中保持连贯性。新模型可以在上下文中保存完整的架构，推理模块如何交互，并且经常产生正确的代码以保持动力。有时，我看到它深入到Next、Vite和React内部来找出bug。最先进的模型令人印象深刻，而且它们似乎一直在变得更好。

---

All of those things had to be true at the same time. Well-documented target API, comprehensive test suite, solid build tool underneath, and a model that could actually handle the complexity. Take any one of them away and this doesn't work nearly as well.

所有这些事情必须同时成立。文档完善的目标API、全面的测试套件、坚实的底层构建工具，以及能够实际处理复杂性的模型。缺少任何一个，效果都会大打折扣。

---

## How we actually built it
## 我们实际是如何构建的

---

Almost every line of code in vinext was written by AI. But here's the thing that matters more: every line passes the same quality gates you'd expect from human-written code. The project has 1,700+ Vitest tests, 380 Playwright E2E tests, full TypeScript type checking via tsgo, and linting via oxlint. Continuous integration runs all of it on every pull request. Establishing a set of good guardrails is critical to making AI productive in a codebase.

vinext中几乎每一行代码都是由AI编写的。但更重要的是：每一行都通过了与人写代码相同的质量门槛。该项目有1,700多个Vitest测试、380个Playwright E2E测试、通过tsgo的完整TypeScript类型检查，以及通过oxlint的lint。持续集成在每个pull request上运行所有这些。建立一套良好的防护措施对于让AI在代码库中高效工作至关重要。

---

The process started with a plan. I spent a couple of hours going back and forth with Claude in [OpenCode](https://opencode.ai) to define the architecture: what to build, in what order, which abstractions to use. That plan became the north star. From there, the workflow was straightforward:

这个过程从计划开始。我花了几个小时在 [OpenCode](https://opencode.ai) 中与Claude来回交流，以定义架构：要构建什么、按什么顺序、使用哪些抽象。这个计划成为了北极星。从那时起，工作流程就很直接了：

---

1. Define a task ("implement the `next/navigation` shim with usePathname, `useSearchParams`, `useRouter`").
2. Let the AI write the implementation and tests.
3. Run the test suite.
4. If tests pass, merge. If not, give the AI the error output and let it iterate.
5. Repeat.

1. 定义任务（"实现带有usePathname、`useSearchParams`、`useRouter`的`next/navigation` shim"）。
2. 让AI编写实现和测试。
3. 运行测试套件。
4. 如果测试通过，合并。如果不通过，给AI错误输出并让它迭代。
5. 重复。

---

We wired up AI agents for code review too. When a PR was opened, an agent reviewed it. When review comments came back, another agent addressed them. The feedback loop was mostly automated.

我们还为代码审查设置了AI代理。当PR打开时，代理会审查它。当审查意见返回时，另一个代理会处理它们。反馈循环大部分是自动化的。

---

It didn't work perfectly every time. There were PRs that were just wrong. The AI would confidently implement something that seemed right but didn't match actual Next.js behavior. I had to course-correct regularly. Architecture decisions, prioritization, knowing when the AI was headed down a dead end: that was all me. When you give AI good direction, good context, and good guardrails, it can be very productive. But the human still has to steer.

它并不每次都完美工作。有些PR就是错的。AI会自信地实现一些看起来正确但与实际Next.js行为不匹配的东西。我必须经常纠正方向。架构决策、优先级排序、知道AI何时走向死胡同：这些都是我。当你给AI良好的方向、良好的上下文和良好的防护措施时，它可以非常高效。但人类仍然必须掌舵。

---

For browser-level testing, I used [agent-browser](https://github.com/vercel-labs/agent-browser) to verify actual rendered output, client-side navigation, and hydration behavior. Unit tests miss a lot of subtle browser issues. This caught them.

对于浏览器级测试，我使用 [agent-browser](https://github.com/vercel-labs/agent-browser) 来验证实际渲染输出、客户端导航和hydration行为。单元测试遗漏了很多微妙的浏览器问题。这捕获了它们。

---

Over the course of the project, we ran over 800 sessions in OpenCode. Total cost: roughly $1,100 in Claude API tokens.

在整个项目过程中，我们在OpenCode中运行了800多个会话。总成本：大约1,100美元的Claude API token。

---

## What this means for software
## 这对软件意味着什么

---

Why do we have so many layers in the stack? This project forced me to think deeply about this question. And to consider how AI impacts the answer.

为什么我们的技术栈中有这么多层？这个项目迫使我深入思考这个问题。并考虑AI如何影响答案。

---

Most abstractions in software exist because humans need help. We couldn't hold the whole system in our heads, so we built layers to manage the complexity for us. Each layer made the next person's job easier. That's how you end up with frameworks on top of frameworks, wrapper libraries, thousands of lines of glue code.

软件中的大多数抽象存在是因为人类需要帮助。我们无法将整个系统装在脑子里，所以我们构建了层来为我们管理复杂性。每一层都让下一个人的工作更容易。这就是为什么你会得到框架之上再堆框架、包装库、数千行胶水代码。

---

AI doesn't have the same limitation. It can hold the whole system in context and just write the code. It doesn't need an intermediate framework to stay organized. It just needs a spec and a foundation to build on.

AI没有同样的限制。它可以在上下文中保存整个系统并直接编写代码。它不需要中间框架来保持组织。它只需要一个规范和一个构建基础。

---

It's not clear yet which abstractions are truly foundational and which ones were just crutches for human cognition. That line is going to shift a lot over the next few years. But vinext is a data point. We took an API contract, a build tool, and an AI model, and the AI wrote everything in between. No intermediate framework needed. We think this pattern will repeat across a lot of software. The layers we've built up over the years aren't all going to make it.

目前还不清楚哪些抽象是真正基础的，哪些只是人类认知的拐杖。这条线在未来几年会发生很大变化。但vinext是一个数据点。我们拿了一个API契约、一个构建工具和一个AI模型，AI编写了中间的一切。不需要中间框架。我们认为这个模式会在很多软件中重复。我们多年来构建的层并非都能留存。

---

## Acknowledgments
## 致谢

---

Thanks to the Vite team. [Vite](https://vite.dev/) is the foundation this whole thing stands on. [`@vitejs/plugin-rsc`](https://github.com/vitejs/vite-plugin-rsc) is still early days, but it gave me RSC support without having to build that from scratch, which would have been a dealbreaker. The Vite maintainers were responsive and helpful as I pushed the plugin into territory it hadn't been tested in before.

感谢Vite团队。[Vite](https://vite.dev/) 是这一切的基础。[`@vitejs/plugin-rsc`](https://github.com/vitejs/vite-plugin-rsc) 还处于早期阶段，但它给了我RSC支持，而不必从头构建，这本来是交易破坏者。当我将插件推向以前未测试过的领域时，Vite维护者反应迅速且乐于助人。

---

We also want to acknowledge the [Next.js](https://nextjs.org/) team. They've spent years building a framework that raised the bar for what React development could look like. The fact that their API surface is so well-documented and their test suite so comprehensive is a big part of what made this project possible. vinext wouldn't exist without the standard they set.

我们还要感谢 [Next.js](https://nextjs.org/) 团队。他们花了多年时间构建了一个提高React开发标准的框架。他们的API表面文档如此完善，测试套件如此全面，这是使这个项目成为可能的重要部分。没有他们设定的标准，vinext就不会存在。

---

## Try it
## 试试看

---

vinext includes an [Agent Skill](https://agentskills.io) that handles migration for you. It works with Claude Code, OpenCode, Cursor, Codex, and dozens of other AI coding tools. Install it, open your Next.js project, and tell the AI to migrate:

vinext包含一个 [Agent Skill](https://agentskills.io)，可以为你处理迁移。它适用于Claude Code、OpenCode、Cursor、Codex和数十种其他AI编码工具。安装它，打开你的Next.js项目，然后告诉AI进行迁移：

---

```javascript
npx skills add cloudflare/vinext
```

---

Then open your Next.js project in any supported tool and say:

然后在任何支持的工具中打开你的Next.js项目并说：

---

```javascript
migrate this project to vinext
```

```javascript
将此项目迁移到vinext
```

---

The skill handles compatibility checking, dependency installation, config generation, and dev server startup. It knows what vinext supports and will flag anything that needs manual attention.

该技能处理兼容性检查、依赖安装、配置生成和开发服务器启动。它知道vinext支持什么，并会标记任何需要手动关注的内容。

---

Or if you prefer doing it by hand:

或者如果你更喜欢手动操作：

---

```javascript
npx vinext init    # Migrate an existing Next.js project
npx vinext dev     # Start the dev server
npx vinext deploy  # Ship to Cloudflare Workers
```

```javascript
npx vinext init    # 迁移现有的Next.js项目
npx vinext dev     # 启动开发服务器
npx vinext deploy  # 部署到Cloudflare Workers
```

---

The source is at [github.com/cloudflare/vinext](https://github.com/cloudflare/vinext). Issues, PRs, and feedback are welcome.

源代码位于 [github.com/cloudflare/vinext](https://github.com/cloudflare/vinext)。欢迎提交issue、PR和反馈。

---

## 批判性思考评论

这篇文章展示了AI在软件开发领域的革命性潜力，同时也引发了一些值得深入思考的问题：

### 1. AI编程的边界与局限

文章强调了这个项目的成功依赖于多个特定条件的对齐：Next.js有完善的文档和测试套件、Vite提供了坚实的基础、AI模型能力达到了新高度。这种"完美风暴"式的条件组合意味着类似的AI主导开发可能难以在所有类型的项目中复制。对于文档不完善、领域知识高度专业化或架构复杂的遗留系统，AI的能力可能会大打折扣。

### 2. 人类角色的转变

虽然AI编写了"几乎每一行代码"，但人类工程师的角色从编码者转变为架构师、指导者和质量控制者。文章坦诚地提到"人类仍然必须掌舵"——AI会自信地实现错误的东西，需要人类进行方向纠正。这揭示了一个关键洞察：AI不会取代工程师，而是改变工程师的工作性质，从实现细节转向更高层次的抽象和判断。

### 3. 关于软件抽象的哲学思考

文章提出了一个深刻的观点：许多软件抽象本质上是"人类认知的拐杖"。AI可以在上下文中保存整个系统，不需要中间框架来保持组织。这让我思考：随着AI能力的提升，我们是否需要重新评估现有的技术栈？哪些抽象是真正必要的，哪些只是为了帮助人类理解而存在的？如果这个观点成立，未来的软件架构可能会发生根本性变化。

### 4. 开源生态系统的权力动态

Cloudflare明确表示希望与其他托管提供商合作，并在Vercel上30分钟内完成了概念验证。这种开放性值得赞赏，但也引发了对权力集中的担忧。如果vinext成为主流，Cloudflare在Workers生态系统中的影响力将进一步扩大。同时，这种"重新实现"而非"适配"的策略，是否会被视为对Next.js/Vercel生态的挑战？

### 5. 实验性项目的生产风险

文章坦诚地标记项目为"实验性"，承认它"还不到一周"且未经过大规模流量测试。然而，他们已经有客户在生产环境中运行它。这种"早期采用者"策略在业界并不罕见，但对于关键业务应用来说，这种程度的"新"是否过于激进？文章中提到的94% API覆盖率意味着仍有6%未覆盖，这可能成为潜在的风险点。

### 6. 成本效益的重新计算

1100美元的token成本相对于传统开发成本来说是惊人的低。但需要考虑的是，这个成本仅包括编码阶段，不包括后续的维护、文档、社区建设等。此外，AI生成的代码虽然通过了测试，但其长期可维护性、可读性和调试难度如何，仍有待观察。

### 7. "流量感知预渲染"的创新性

TPR概念利用Cloudflare作为反向代理的优势，基于实际流量数据决定预渲染哪些页面，这是一个聪明的设计。它挑战了传统的"构建时预渲染一切"的模式，可能代表了静态站点生成（SSG）范式的演进方向。然而，这也引入了对外部服务（Cloudflare分析）的依赖，以及可能的数据隐私考虑。

总的来说，这篇文章不仅是一个技术成果的展示，更是一个关于AI如何改变软件开发本质的案例研究。它既令人兴奋——展示了AI的巨大潜力；也令人警醒——提醒我们重新思考软件工程的基本假设。vinext可能是一个标志性项目，标志着AI辅助/主导开发的新时代的开始。
