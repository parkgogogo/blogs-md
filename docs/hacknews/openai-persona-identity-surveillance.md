# The Watchers: How OpenAI, the US Government, and Persona Built an Identity Surveillance Machine
# 观察者：OpenAI、美国政府与 Persona 如何构建身份监控机器

**Source**: https://vmfunc.re/blog/persona/  
**Authors**: vmfunc, MDL, Dziurwa  
**Date**: February 16, 2026

---

## Executive Summary

This investigative report reveals how OpenAI and identity verification company Persona collaborate on a comprehensive identity surveillance system that screens millions of users monthly. Through passive reconnaissance of publicly accessible infrastructure, the authors discovered 53MB of unprotected source code from a FedRAMP-authorized government endpoint, exposing the full architecture of a platform that:

- Files Suspicious Activity Reports (SARs) directly with FinCEN
- Maintains biometric face databases with 3-year retention
- Runs 269 distinct verification checks per user
- Compares selfies to political figures using facial recognition
- Tags reports with intelligence program codenames

The same codebase powers both OpenAI's consumer identity verification and Persona's government-facing platform.

---

## 执行摘要

这篇调查报告揭示了 OpenAI 与身份验证公司 Persona 如何合作构建一个全面的身份监控系统，每月筛选数百万用户。通过对公开可访问基础设施的被动侦察，作者从一个 FedRAMP 授权的政府端点发现了 53MB 未受保护的源代码，暴露了一个平台的完整架构，该平台：

- 直接向 FinCEN（金融犯罪执法网络）提交可疑活动报告
- 维护生物识别面部数据库，保留期长达 3 年
- 对每个用户运行 269 项不同的验证检查
- 使用面部识别将自拍与政治人物进行比对
- 使用情报项目代码名称标记报告

同一套代码库同时支持 OpenAI 的消费者身份验证和 Persona 面向政府的平台。

---

## Prologue: The Discovery

It started with a Shodan search. A single IP address (`34.49.93.177`) on Google Cloud in Kansas City. One open port. Two SSL certificate hostnames that told a story nobody was supposed to read:

```
openai-watchlistdb.withpersona.com
openai-watchlistdb-testing.withpersona.com
```

Not "openai-verify", not "openai-kyc", but **watchlistdb**.

---

## 序言：发现

这一切始于一次 Shodan 搜索。一个位于堪萨斯城 Google Cloud 上的 IP 地址（`34.49.93.177`）。一个开放端口。两个 SSL 证书主机名，讲述了一个不该被阅读的故事：

```
openai-watchlistdb.withpersona.com
openai-watchlistdb-testing.withpersona.com
```

不是 "openai-verify"，不是 "openai-kyc"，而是 **watchlistdb（观察名单数据库）**。

---

## The Infrastructure

### OpenAI Watchlist Database

| Attribute | Value |
|-----------|-------|
| IP | 34.49.93.177 |
| Provider | Google Cloud (AS396982) |
| Location | Kansas City, US |
| Hostnames | openai-watchlistdb.withpersona.com, openai-watchlistdb-testing.withpersona.com |
| First Seen | November 16, 2023 |

The service has been operational for over **27 months**—predating OpenAI's public announcement of identity verification requirements by 18 months.

---

## 基础设施

### OpenAI 观察名单数据库

| 属性 | 值 |
|------|-----|
| IP | 34.49.93.177 |
| 提供商 | Google Cloud (AS396982) |
| 位置 | 美国堪萨斯城 |
| 主机名 | openai-watchlistdb.withpersona.com, openai-watchlistdb-testing.withpersona.com |
| 首次发现 | 2023年11月16日 |

该服务已运行超过 **27 个月**——比 OpenAI 公开发布身份验证要求早了 18 个月。

---

## Certificate Transparency Timeline

| Date | Event |
|------|-------|
| 2023-11-16 | **Service goes live** |
| 2024-02-28 | Testing environment gets own certificate |
| 2025-10-07 | Persona achieves FedRAMP Authorized status |
| 2026-02-04 | "ONYX" deployment appears |
| 2026-01-24 | Current certificate issued |

---

## 证书透明度时间线

| 日期 | 事件 |
|------|------|
| 2023-11-16 | **服务上线** |
| 2024-02-28 | 测试环境获得独立证书 |
| 2025-10-07 | Persona 获得 FedRAMP 授权状态 |
| 2026-02-04 | "ONYX" 部署出现 |
| 2026-01-24 | 当前证书颁发 |

---

## The 269 Verification Checks

Source code analysis revealed **269 distinct verification checks** across 14 categories:

### Selfie Checks (23 checks)
- `SelfieIdComparison` - Face vs ID photo match
- `SelfiePublicFigureDetection` - Do you look like someone famous?
- `SelfieSuspiciousEntityDetection` - "Suspicious" face detection
- `SelfieExperimentalModelDetection` - Unnamed ML models on your face
- `SelfieAgeComparison` - Age estimation from face
- `SelfieFaceCoveringDetection` - Mask detection
- `SelfiePoseRepeatDetection` - Same pose as another user

### Government ID Checks (43 checks)
- AAMVA database lookup (US driver's license)
- Physical tamper detection
- NFC chip reading with PKI validation
- Real ID detection

### Database Checks (27 checks)
- Deceased detection (SSA death master file)
- Social Security number validation
- Phone carrier verification
- Aadhaar (India) database checks

### Document Checks (29 checks)
- JPEG original image detection
- PDF editor detection
- Synthetic content detection
- Digital text modification detection

---

## 269 项验证检查

源代码分析揭示了跨越 14 个类别的 **269 项不同验证检查**：

### 自拍检查（23 项）
- `SelfieIdComparison` - 面部与证件照片比对
- `SelfiePublicFigureDetection` - 你是否看起来像某个名人？
- `SelfieSuspiciousEntityDetection` - "可疑"面部检测
- `SelfieExperimentalModelDetection` - 在你的面部上运行未命名的 ML 模型
- `SelfieAgeComparison` - 从面部估计年龄
- `SelfieFaceCoveringDetection` - 口罩检测
- `SelfiePoseRepeatDetection` - 与其他用户姿势相同

### 政府证件检查（43 项）
- AAMVA 数据库查询（美国驾照）
- 物理篡改检测
- 带 PKI 验证的 NFC 芯片读取
- Real ID 检测

### 数据库检查（27 项）
- 死亡检测（SSA 死亡主文件）
- 社会安全号码验证
- 电话运营商验证
- Aadhaar（印度）数据库检查

### 文档检查（29 项）
- JPEG 原始图像检测
- PDF 编辑器检测
- 合成内容检测
- 数字文本修改检测

---

## The Source Code Leak

On February 4, 2026, researchers discovered unprotected JavaScript source maps on `app.onyx.withpersona-gov.com/vite-dev/`:

- **53 megabytes** of TypeScript source code
- **2,456 source files**
- Served **without authentication**
- From a **FedRAMP-authorized government endpoint**

The source maps contained:
- Complete API endpoint definitions
- Internal permission systems
- Screening algorithm implementations
- Database schema references

---

## 源代码泄露

2026年2月4日，研究人员在 `app.onyx.withpersona-gov.com/vite-dev/` 上发现了未受保护的 JavaScript 源代码映射：

- **53 MB** TypeScript 源代码
- **2,456 个源文件**
- **无需认证**即可访问
- 来自 **FedRAMP 授权的政府端点**

源代码映射包含：
- 完整的 API 端点定义
- 内部权限系统
- 筛选算法实现
- 数据库模式引用

---

## SAR Filing to FinCEN

The platform includes a complete Suspicious Activity Report (SAR) module for direct filing with FinCEN (Financial Crimes Enforcement Network, US Treasury).

**Source files:**
- `dashboard/views/DashboardSARShowView/DashboardSARShowView.tsx`
- `dashboard/models/filing.ts`

**Key functions:**
```typescript
handleAutofillSAR()      // Autofill from case data
handleValidateSAR()      // Validate against FinCEN XML schema
handleFileSAR()          // File electronically
handleExportFincenPDF()  // Export FinCEN PDF
```

**SAR Status Lifecycle:**
```typescript
enum FincenStatus {
  Open = 'open',
  Pending = 'pending',
  FiledElectronically = 'filed_electronically',
  Accepted = 'accepted',
  AcceptedWithWarnings = 'accepted_with_warnings',
  Rejected = 'rejected',
  Archived = 'archived',
}
```

---

## 向 FinCEN 提交 SAR

该平台包含一个完整的可疑活动报告（SAR）模块，用于直接向 FinCEN（金融犯罪执法网络，美国财政部）提交报告。

**源文件：**
- `dashboard/views/DashboardSARShowView/DashboardSARShowView.tsx`
- `dashboard/models/filing.ts`

**关键函数：**
```typescript
handleAutofillSAR()      // 从案例数据自动填充
handleValidateSAR()      // 根据 FinCEN XML 模式验证
handleFileSAR()          // 电子提交
handleExportFincenPDF()  // 导出 FinCEN PDF
```

**SAR 状态生命周期：**
```typescript
enum FincenStatus {
  Open = 'open',                          // 开放
  Pending = 'pending',                    // 待处理
  FiledElectronically = 'filed_electronically',  // 已电子提交
  Accepted = 'accepted',                  // 已接受
  AcceptedWithWarnings = 'accepted_with_warnings',  // 带警告接受
  Rejected = 'rejected',                  // 已拒绝
  Archived = 'archived',                  // 已归档
}
```

---

## The Architecture

```
User (signs up for OpenAI)
    ↓
Persona Verification Flow
    - Government ID scan (Microblink)
    - Selfie capture + liveness detection
    - Video capture
    - Public figure facial matching
    - Device fingerprint (FingerprintJS)
    ↓
openai-watchlistdb.withpersona.com
    - Screens against OFAC SDN list
    - 200+ global sanctions lists
    - PEP classes 1-4 (facial similarity)
    - Adverse media (14 categories)
    - Crypto address watchlists
    ↓
OpenAI (grants or denies access)
```

Meanwhile, the government platform (`withpersona-gov.com`) runs the **same codebase** with additional capabilities:
- Files SARs to FinCEN
- Files STRs to FINTRAC (Canada)
- Tags reports with intelligence codenames
- Biometric retention: 3 years
- 13 types of tracking lists

---

## 架构

```
用户（注册 OpenAI）
    ↓
Persona 验证流程
    - 政府证件扫描（Microblink）
    - 自拍采集 + 活体检测
    - 视频采集
    - 公众人物面部匹配
    - 设备指纹（FingerprintJS）
    ↓
openai-watchlistdb.withpersona.com
    - 针对 OFAC SDN 名单筛选
    - 200+ 全球制裁名单
    - PEP 1-4 级（面部相似度）
    - 负面媒体（14 个类别）
    - 加密货币地址观察名单
    ↓
OpenAI（授予或拒绝访问）
```

同时，政府平台（`withpersona-gov.com`）运行 **相同的代码库**，具有额外功能：
- 向 FinCEN 提交 SAR
- 向 FINTRAC（加拿大）提交 STR
- 使用情报代码名称标记报告
- 生物识别保留期：3 年
- 13 种类型的跟踪名单

---

## Key Questions Raised

1. What was OpenAI screening against in November 2023, 18 months before disclosing identity verification?

2. Does "watchlistdb" imply a proprietary watchlist beyond OFAC/SDN/PEP?

3. What defines a "suspicious entity" in `SelfieSuspiciousEntityDetection`?

4. What do the experimental model detection checks do? Unnamed ML models on biometric data.

5. What is the actual biometric retention period? OpenAI says "up to a year." The code says 3 years.

6. Why is Ukraine blocked alongside OFAC-sanctioned countries when Ukraine itself is not sanctioned?

7. Is there a direct pipeline between OpenAI's millions of monthly screenings and the government SAR filing system?

---

## 提出的关键问题

1. OpenAI 在 2023 年 11 月（比披露身份验证早 18 个月）针对什么进行筛选？

2. "watchlistdb" 是否意味着除了 OFAC/SDN/PEP 之外的专有观察名单？

3. `SelfieSuspiciousEntityDetection` 如何定义"可疑实体"？

4. 实验性模型检测检查做什么？在生物识别数据上运行未命名的 ML 模型。

5. 实际的生物识别保留期是多久？OpenAI 说"最多一年"。代码显示 3 年。

6. 为什么乌克兰与 OFAC 制裁国家一起被封锁，而乌克兰本身并未受制裁？

7. OpenAI 每月数百万次筛选与政府 SAR 提交系统之间是否存在直接通道？

---

## Methodology

All findings obtained through **passive reconnaissance** using publicly available tools:

- Shodan (shodan.io)
- Certificate Transparency logs (crt.sh)
- DNS resolution
- HTTP/HTTPS requests to public endpoints
- SSL/TLS certificate inspection
- JavaScript source map analysis (publicly served)

**What was NOT done:**
- No authentication attempts
- No vulnerability scanning
- No exploitation
- No brute-forcing
- No data modification

---

## 方法论

所有发现均通过使用公开可用工具的 **被动侦察** 获得：

- Shodan (shodan.io)
- 证书透明度日志 (crt.sh)
- DNS 解析
- 对公共端点的 HTTP/HTTPS 请求
- SSL/TLS 证书检查
- JavaScript 源代码映射分析（公开提供）

**未做的事情：**
- 无认证尝试
- 无漏洞扫描
- 无利用
- 无暴力破解
- 无数据修改

---

## Legal Notice (from original)

> No laws were broken. All findings come from passive recon using public sources - Shodan, CT logs, DNS, HTTP headers, and unauthenticated files served by the target's own web server. No systems were accessed, no credentials were used, no data was modified.

> Retrieving publicly served files is not unauthorized access - see *Van Buren v. United States* (593 U.S. 374, 2021), *hiQ Labs v. LinkedIn* (9th Cir. 2022).

---

## 法律声明（来自原文）

> 未违反任何法律。所有发现均来自使用公共来源的被动侦察——Shodan、CT 日志、DNS、HTTP 标头以及目标自己 Web 服务器提供的未经认证的文件。未访问任何系统，未使用任何凭证，未修改任何数据。

> 检索公开提供的文件不属于未经授权的访问——参见 *Van Buren v. United States* (593 U.S. 374, 2021)、*hiQ Labs v. LinkedIn* (第九巡回法院 2022)。

---

## Conclusion

The same company that takes your passport photo when you sign up for ChatGPT operates a government platform that files Suspicious Activity Reports with FinCEN. Same codebase. Same platform. Different deployment.

**2,456 source files. 269 verification checks. 13 list types. 3-year biometric retention.**

The information is the moral argument.

---

## 结论

当你注册 ChatGPT 时拍摄护照照片的公司，同时运营着向 FinCEN 提交可疑活动报告的政府平台。相同的代码库。相同的平台。不同的部署。

**2,456 个源文件。269 项验证检查。13 种名单类型。3 年生物识别保留期。**

信息就是道德论据。

---

*End of translation. Original article: https://vmfunc.re/blog/persona/*  
*翻译结束。原文：https://vmfunc.re/blog/persona/*
