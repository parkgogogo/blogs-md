---
title: "OpenAI, the US government and Persona built an identity surveillance machine"
url: "https://vmfunc.re/blog/persona/"
rating: 9
category: "Privacy/Security"
date: "2026-02-28"
---

# OpenAI, the US government and Persona built an identity surveillance machine

## ADDENDUM — february 18, 2026

we are in direct written correspondence with persona’s CEO, rick song. he has been responsive and engaged in good faith.

rick has committed to answering the 18 questions in 0x14 in writing. all correspondence will be published in full as part 2 of this series. the core findings, including openai-watchlistdb.withpersona.com and its 27 months of certificate transparency history, remain unaddressed.

> **LEGAL NOTICE**
>
> **no laws were broken.** all findings come from passive recon using public sources - Shodan, CT logs, DNS, HTTP headers, and unauthenticated files served by the target’s own web server. no systems were accessed, no credentials were used, no data was modified. retrieving publicly served files is not unauthorized access - see *Van Buren v. United States* (593 U.S. 374, 2021), *hiQ Labs v. LinkedIn* (9th Cir. 2022).
>
> this is protected journalism and security research under the First Amendment, ECHR Art. 10, CFAA safe harbor (DOJ Policy 2022), California Shield Law, GDPR Art. 85, and Israeli Basic Law: Human Dignity and Liberty.
>
> the authors are not affiliated with any government, intelligence service, or competitor of any entity named herein. no financial interest. no compensation. this research exists in the public interest and was distributed across multiple jurisdictions, dead drops, and third-party archives before publication.
>
> any attempt to suppress or retaliate against this publication - legal threats, DMCA abuse, employment interference, physical intimidation, or extrajudicial action - will be treated as confirmation of its findings and will trigger additional distribution. killing the messenger does not kill the message.
>
> **for the record:** all authors of this document are in good health, of sound mind, and have no plans to hurt themselves, disappear, or die unexpectedly. if that changes suddenly - it wasn’t voluntary. this document, its evidence, and a list of names are held by multiple trusted third parties with instructions to publish everything in the event that anything happens to any of us. we mean anything.
>
> to Persona and OpenAI’s legal teams: actually audit your supposed “FedRAMP” compliancy, and answer the questions in 0x14. that’s the appropriate response. everything else is the wrong one.

```plaintext
from:     the world
to:       openai, persona, the US government, ICE, the open internet
date:     2026-02-16
subject:  the watchers
```

---

### *greetz from [vmfunc](https://twitter.com/vmfunc), [MDL](https://twitter.com/mdlcsgo), [Dziurwa](https://github.com/Dziurwa14)*

---

they told us the future would be convenient. sign up, verify your identity, talk to the machine. easy. frictionless. the brochure said “trust and safety.” the source code said `SelfieSuspiciousEntityDetection`.

funny how that works. you hand over your passport to use a chatbot and somewhere in a datacenter in iowa, a facial recognition algorithm is checking whether you look like a politically exposed person. your selfie gets a similarity score. your name hits a watchlist. a cron job re-screens you every few weeks just to make sure you haven’t become a terrorist since the last time you asked GPT to write a cover letter.

so what do you do? well, we looked. found source code on a government endpoint with the door wide open. facial recognition, watchlists, SAR filings, intelligence codenames, and much more.

oh, and we revealed the names of every single person responsible for this!!

---

## 0x00 - prologue

following the works of [eva](https://twitter.com/xyz3va) and others on ID verification bypasses, we decided to start looking into [persona](https://withpersona.com), yet another KYC service that uses facial recognition to verify identities. the original goal was to add a age-verification bypass to eva’s existing k-id platform.

after trying to write a few exploits, vmfunc decided to browse their infra on shodan. it all started with a Shodan search. a single IP. `34.49.93.177` sitting on Google Cloud in Kansas City. one open port. one SSL certificate. two hostnames that tell a story nobody was supposed to read:

```plaintext
openai-watchlistdb.withpersona.com
openai-watchlistdb-testing.withpersona.com
```

not “openai-verify”, not “openai-kyc”, **watchlistdb.** a database. (or is it?)

it was initially meant to be a passive recon investigation, that quickly turned into a rabbit hole deep dive into how commercial AI and federal government operations work together to violate our privacy every waking second. we didn’t even have to write or perform a single exploit, the entire architecture was just on the doorstep!! 53 megabytes of unprotected source maps on a `FedRAMP` government endpoint, exposing the entire codebase of a platform that files Suspicious Activity Reports with `FinCEN`, compares your selfie to watchlist photos using facial recognition, screens you against 14 categories of adverse media from terrorism to espionage, and tags reports with codenames from active intelligence programs.

2,456 source files containing the full TypeScript codebase, every permission, every API endpoint, every compliance rule, every screening algorithm. sitting unauthenticated on the public internet. on a government platform no less.

no systems were breached. no credentials were used. every finding in this document comes from publicly accessible sources: shodan, certificate transparency logs, DNS resolution, HTTP response headers, published API documentation, public web pages, and unauthenticated JavaScript source maps served by the target’s own web server.

the infrastructure told its own story. we just listened. then we read the source code.

## 0x01 - the target: 34.49.93.177

```plaintext
IP:             34.49.93.177
ASN:            AS396982 (Google LLC)
provider:       Google Cloud
region:         global
city:           Kansas City, US
open ports:     443/tcp
last seen:      2026-02-05

hostnames:
  - 177.93.49.34.bc.googleusercontent.com
  - openai-watchlistdb.withpersona.com
  - openai-watchlistdb-testing.withpersona.com

SSL cert:
  subject:      CN=openai-watchlistdb.withpersona.com
  issuer:       C=US, O=Google Trust Services, CN=WR3
  valid:        Jan 24 01:24:11 2026 - Apr 24 02:20:06 2026
  SANs:         openai-watchlistdb.withpersona.com
                openai-watchlistdb-testing.withpersona.com
  serial:       FDFFBF37ED89BBD710D9967B7CD92B52

HTTP response (all paths, all methods):
  status:       404
  body:         "fault filter abort"
  headers:      via: 1.1 google
                content-type: text/plain
                Alt-Svc: h3=":443"
```

## 0x02 - dedicated infrastructure

Persona (withpersona.com) is a San Francisco-based identity verification company. their normal infrastructure runs behind Cloudflare:

```plaintext
withpersona.com          -> 162.159.141.40, 172.66.1.36  (CF)
inquiry.withpersona.com  -> 162.159.141.40, 172.66.1.36  (CF)
app.withpersona.com      -> 162.159.141.40, 172.66.1.36  (CF)
api.withpersona.com      -> 162.159.141.40, 172.66.1.36  (CF)
```

HOWEVER, OpenAI’s watchlist service breaks out of this wildcard:

```plaintext
openai-watchlistdb.withpersona.com         -> 34.49.93.177  (GCP)
openai-watchlistdb-testing.withpersona.com -> 34.49.93.177  (GCP)
```

## 0x03 - certificate transparency timeline

CT logs tell us exactly when this service went live and how it evolved.

november 2023. this service has been running for over two years.

OpenAI didn’t announce “Verified Organization” requirements until mid-2025. they didn’t publicly require ID verification for advanced model access until GPT-5. but the watchlist screening infrastructure was operational 18 months before any of that was disclosed.

## 0x04 - what the API reveals

Persona’s API documentation is public. when a customer like OpenAI runs a government ID verification, the API returns a complete identity dossier:

```plaintext
personal identity:
  - full legal name (including native script)
  - date of birth, place of birth
  - nationality, sex, height

address:
  - street, city, state, postal code, country

government document:
  - document type and number
  - issuing authority
  - issue and expiration dates
  - visa status

media:
  - FRONT PHOTO of ID document (URL)
  - BACK PHOTO of ID document (URL)
  - SELFIE PHOTO (URL + byte size)
  - VIDEO of identity capture (URL)

metadata:
  - entity confidence score
  - all verification check results with pass/fail reasons
  - capture method used
  - timestamps (created, submitted, completed, redacted)
```

## 0x05 - the government platform: withpersona-gov.com

```plaintext
IP:             34.27.15.233
ASN:            AS396982 (Google LLC)
provider:       Google Cloud, us-central1
city:           Council Bluffs, US
open ports:     80 (redirect), 443
cert:           CN=*.withpersona-gov.com (wildcard)
tech:           Caddy web server, Go, Google Cloud CDN
```

Persona achieved FedRAMP Authorized status at the Low Impact level on October 7, 2025.

## 0x06 - the CSP header leak

the Content-Security-Policy header from withpersona-gov.com leaked their vendor/integration stack, including:

- **api.openai.com**
- **FingerprintJS**
- **Microblink**
- **Sentry**
- **Amplitude** + **Pendo**
- **Datadog RUM**
- **MX/MoneyDesktop**

## 0x07 - the ONYX deployment

on february 4, 2026, `onyx.withpersona-gov.com` appeared in CT logs, with dedicated GCP infra, its own wildcard cert, and `persona-onyx` k8s namespace.

## 0x08 - the source maps: 53 megabytes of naked code

on `app.onyx.withpersona-gov.com/dashboard/login`, the `/vite-dev/` path served JS source maps without authentication, exposing full TypeScript sources.

```plaintext
17 source map files, 53 MB total
extracted: 2,456 total source files
directories: front-end/ (2,056), app/ (400)
file types: TypeScript, CSS, JSON, SVG
```

## 0x09 - SAR: filing suspicious activity reports directly to FinCEN

source files referenced:
- `dashboard/views/DashboardSARShowView/DashboardSARShowView.tsx`
- `dashboard/views/DashboardSARShowView/components/SARInstructionsCard.tsx`
- `dashboard/models/filing.ts`

the platform includes full SAR lifecycle operations, including direct filing to FinCEN.

## 0x0A - STR: filing to FINTRAC with intelligence program tags

source files referenced:
- `dashboard/views/DashboardFilingShowView/components/STRFormSchema.tsx`
- `dashboard/lib/filing/strs/customValidate.ts`
- `dashboard/models/filing.ts`

includes STR filing to FINTRAC and hardcoded project-name tags such as:
- Project ANTON
- Project ATHENA
- Project CHAMELEON
- Project GUARDIAN
- Project LEGION
- Project PROTECT
- Project SHADOW

## 0x0B - face lists: biometric databases with 3-year retention

source files referenced:
- `dashboard/components-lib/AsyncSelfie/AsyncSelfie.tsx`
- `dashboard/views/DashboardListsView/AddListModal.tsx`
- `dashboard/lib/constants/list.ts`

face/selfie data can be added to list systems with max biometric retention of 3 years.

## 0x0C - the OpenAI integration

source files referenced:
- `dashboard/hooks/useAgentConversationStream.ts`
- `lib/constants/externalIntegrationVendors.ts`

OpenAI appears as `ExternalIntegrationProductivityOpenAi`, described as an operator copilot integration.

## 0x0D - watchlist screening

screening options include sanctions, PEP, adverse media, recurring re-screening, fuzzy matching, transliteration matching, and custom FinCEN list upload formats.

## 0x0E - PEP facial recognition

source files:
- `PoliticallyExposedPersonV2EntityMatchDetails.tsx`
- `PoliticallyExposedPersonPhotoComparison.tsx`

shows selfie-vs-reference portrait comparison with similarity levels `low | medium | high`.

## 0x0F - chainalysis crypto address surveillance

source file:
- `dashboard/components/ReportResult/ChainalysisAddressScreening.tsx`

includes risk levels, cluster analysis, exposure amounts, and recurring watchlist rescreening.

## 0x10 - the full verification pipeline: 269 checks

source file: `lib/verificationCheck.ts`

the enum lists 269 checks across selfie, gov-ID, database, document, and business verification categories.

## 0x11 - the architecture

article includes an end-to-end architecture diagram from user signup to Persona screening systems and government platform overlaps.

## 0x12 - the legal questions

the article raises concerns including:
- Ukraine blocking policy vs OFAC scope
- biometric retention discrepancy (1 year vs 3 years vs “permanent”)
- potential BIPA exposure
- transparency/appeal absence

## 0x13 - what the code does NOT show

authors state they found no direct evidence of:
- ICE integration in code
- direct Fivecast ONYX product references in code
- classic law-enforcement surveillance vendor SDKs
- direct bidirectional OpenAI surveillance pipeline

## 0x14 - questions that deserve answers

the article lists 18 pointed questions to Persona/OpenAI/government stakeholders about screening purpose, data retention, model criteria, legal compliance, transparency, and governance.

## 0x15 - infrastructure reference

the article provides a full infra matrix for production/staging/gov/ONYX/trust endpoints, providers, cert timing, and observed services.

## 0x16 - methodology

passive recon only:
- Shodan
- crt.sh
- DNS
- HTTP/TLS headers
- public docs
- publicly served source maps
- static code analysis

states no auth attempts, exploitation, brute forcing, or data modification.

## 0x17 - epilogue

the article concludes that one shared company/platform stack appears across consumer identity screening and government compliance tooling, and argues this raises major civil-liberty and governance questions.

## 0x18 - betrayal

the original post includes a discussion about individuals connected to development ecosystems and an addendum noting the author removed a previously posted list of names.

## sources

(See original article for full source links and evidence references.)

---

# 中文翻译

## 补充说明 —— 2026 年 2 月 18 日

我们正在与 Persona CEO Rick Song 进行书面沟通。对方有回应，并表现出善意协商态度。

Rick 承诺会就 0x14 中的 18 个问题给出书面答复。全部往来将作为本系列第 2 部分完整公开。核心发现（包括 `openai-watchlistdb.withpersona.com` 以及其 27 个月证书透明日志历史）仍未被正面回应。

> **法律声明**
>
> **没有违法行为。** 所有发现均来自公开来源的被动侦察：Shodan、CT 日志、DNS、HTTP 头，以及目标服务器公开提供的未认证文件。未访问受限系统、未使用凭证、未修改数据。获取公开提供文件不构成未授权访问。
>
> 本文属于受保护的新闻与安全研究活动。

```plaintext
from:     the world
to:       openai, persona, the US government, ICE, the open internet
date:     2026-02-16
subject:  the watchers
```

---

### *来自 [vmfunc](https://twitter.com/vmfunc)、[MDL](https://twitter.com/mdlcsgo)、[Dziurwa](https://github.com/Dziurwa14) 的问候*

---

他们告诉我们未来会很方便：注册、验证身份、和机器对话。简单、无摩擦。宣传册写的是“信任与安全”，源码里写的是 `SelfieSuspiciousEntityDetection`。

这就是荒诞之处：你为了用聊天机器人提交护照，而在爱荷华某个数据中心里，面部识别算法正在判断你是否像“政治公众人物（PEP）”。你的自拍会得到相似度分数，你的名字会命中观察名单，cron 任务还会每隔几周复筛一次，确认你自上次让 GPT 写求职信之后有没有“变成恐怖分子”。

于是我们去查了。结果在一个政府端点上发现了几乎敞开的源码：人脸识别、观察名单、SAR 申报、情报代号等等。

## 0x00 - 前言

受 [eva](https://twitter.com/xyz3va) 等人关于身份验证绕过研究的启发，我们开始调查 [persona](https://withpersona.com) —— 另一个使用人脸识别做 KYC 的服务。

一切始于一次 Shodan 搜索：`34.49.93.177`。该 IP 位于 Google Cloud（堪萨斯城），开放端口只有一个，证书一个，却暴露了两个关键主机名：

```plaintext
openai-watchlistdb.withpersona.com
openai-watchlistdb-testing.withpersona.com
```

不是 `openai-verify`，不是 `openai-kyc`，而是 **watchlistdb**。

作者称原本只是被动侦察，后来演变成对“商业 AI 与联邦政府协作隐私监控机制”的深挖。其核心说法是：在一个 `FedRAMP` 政府端点上发现了 53MB 未保护 source map，可重建完整 TypeScript 代码树，涉及 FinCEN SAR、人脸与名单比对、14 类负面媒体筛查与情报项目标签等。

## 0x01 - 目标：34.49.93.177

```plaintext
IP:             34.49.93.177
ASN:            AS396982 (Google LLC)
provider:       Google Cloud
city:           Kansas City, US
open ports:     443/tcp
hostnames:
  - openai-watchlistdb.withpersona.com
  - openai-watchlistdb-testing.withpersona.com
```

## 0x02 - 专用基础设施

Persona 常规域名通常在 Cloudflare 后面，但 OpenAI 的 watchlist 服务解析到独立 GCP IP（`34.49.93.177`），与共享入口不同。

## 0x03 - 证书透明时间线

CT 日志显示该服务自 2023 年 11 月开始运行，早于 OpenAI 对外公开相关身份验证策略的时间。

## 0x04 - API 可见信息

Persona 公共 API 文档显示，政府 ID 验证可返回完整身份档案：姓名、出生信息、国籍、住址、证件信息、自拍/证件图/视频 URL、以及验证结果与时间戳等。

## 0x05 - 政府平台：withpersona-gov.com

文章识别出 `withpersona-gov.com` 的并行部署（GCP），并提到 Persona 于 2025-10-07 达成 FedRAMP Low 授权。

## 0x06 - CSP 头信息泄露

CSP 头暴露了其集成生态：
- `api.openai.com`
- FingerprintJS
- Microblink
- Sentry
- Amplitude / Pendo
- Datadog RUM
- MX/MoneyDesktop

## 0x07 - ONYX 部署

2026-02-04 起，`onyx.withpersona-gov.com` 出现在 CT 日志中，具备独立证书与 K8s 命名空间 `persona-onyx`。

## 0x08 - 53MB source maps

文章称在 `app.onyx.withpersona-gov.com/dashboard/login` 的 `/vite-dev/` 路径上可未认证获取 source map，重建出 2,456 个源码文件。

```plaintext
17 个 source map，总计 53MB
提取源码：2,456 文件
目录：front-end (2,056) + app (400)
```

## 0x09 - 直连 FinCEN 的 SAR 申报

引用源码路径显示该平台具备 SAR 创建、校验、导出与电子提交流程，含 “Send to FinCEN” 相关能力。

## 0x0A - 直连 FINTRAC 的 STR 申报 + 情报项目标签

文章称 STR 表单与 FINTRAC 报送结构对应，并存在硬编码项目标签（如 Project SHADOW、Project LEGION）。

## 0x0B - 人脸名单库与 3 年保留

文中指出系统支持多类名单（身份证号、IP、姓名、设备指纹、地理位置、人脸等），其中人脸类为增强类型，保留上限 3 年。

## 0x0C - OpenAI 集成

源码中 OpenAI 被归类为生产力集成（类似 Slack/Zendesk），主要表现为运营人员 AI Copilot 流式会话能力。

## 0x0D - 名单筛查能力

配置层面包含制裁、PEP、负面媒体、复筛周期、模糊匹配、转写匹配、自定义 FinCEN 文件格式等。

## 0x0E - PEP 人脸相似度比对

文章称 PEP V2 视图支持自拍与参考照并排比对，输出 `low | medium | high` 相似等级。

## 0x0F - Chainalysis 加密地址监控

包含风险级别、地址簇分析、金额暴露、并可做周期性复筛。

## 0x10 - 269 项验证检查

`lib/verificationCheck.ts` 被描述为包含 269 项校验，覆盖自拍、证件、数据库、文档与企业维度。

## 0x11 - 架构总结

文章给出端到端流程：用户提交身份资料 → Persona 验证/筛查体系 → 决策通过或拒绝；并强调其政府平台侧与消费平台侧在代码与数据模型上的重合。

## 0x12 - 法律问题

核心争议包括：
- 乌克兰封禁策略与 OFAC 范围关系
- 生物特征保留时长披露不一致（1 年 / 3 年 / 永久）
- BIPA 风险
- 拒绝后缺乏解释与申诉

## 0x13 - 代码未直接证明的部分

作者同时声明：未在代码中直接发现 ICE 集成、Fivecast ONYX 产品层显式连接、典型执法监控厂商 SDK、或 OpenAI 双向监控数据管道的明确证据。

## 0x14 - 18 个待答复问题

文中列出 18 个问题，围绕：筛查起始时间、watchlistdb 定义、模型标准、保留策略、合规性、透明度、以及治理责任。

## 0x15 - 基础设施索引

给出生产/预发/政府/ONYX/Trust 的域名、IP、证书与观察到的服务信息。

## 0x16 - 方法论

强调仅做被动公开信息分析：Shodan、CT、DNS、HTTP/TLS、公开文档、公开 source map 与静态代码分析；未做认证尝试、漏洞利用、暴力破解、数据修改。

## 0x17 - 结语

文章观点是：同一家公司在消费级身份核验与政府合规系统两侧运行高度相似的平台能力，这本身就足以引发重大的隐私、权力与问责问题。

## 0x18 - betrayal

原文最后还讨论了开发者群体与监督责任，并在 2 月 18 日补充说明中表示已移除先前公开的人名列表。

## sources

详见原文页面中的外部链接与证据引用。
