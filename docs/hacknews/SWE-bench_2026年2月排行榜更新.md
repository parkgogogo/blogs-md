# SWE-bench February 2026 Leaderboard Update / SWE-bench 2026年2月排行榜更新

**Original URL / 原文链接**: https://simonwillison.net/2026/Feb/19/swe-bench/

**Tags / 标签**: `SWE-bench`, `AI Benchmark`, `Code Generation`, `LLM`, `Claude`, `GPT`, `Gemini`, `DeepSeek`

---

## Main Content / 正文

[SWE-bench February 2026 leaderboard update](https://www.swebench.com/) ([via](https://twitter.com/KLieret/status/2024176335782826336))

[SWE-bench 2026年2月排行榜更新](https://www.swebench.com/)（[来源](https://twitter.com/KLieret/status/2024176335782826336)）

SWE-bench is one of the benchmarks that the labs love to list in their model releases. The official leaderboard is infrequently updated but they just did a full run of it against the current generation of models, which is notable because it's always good to see benchmark results like this that weren't self-reported by the labs.

SWE-bench 是各大实验室在发布模型时都喜欢引用的基准测试之一。官方排行榜更新频率不高，但他们刚刚针对当前这一代模型进行了一次完整测试，这值得关注——因为能看到这种并非由实验室自行报告的基准测试结果总是好事。

The fresh results are for their "Bash Only" benchmark, which runs their [mini-swe-bench](https://github.com/SWE-agent/mini-swe-agent) agent (~9,000 lines of Python, [here are the prompts](https://github.com/SWE-agent/mini-swe-agent/blob/v2.2.1/src/minisweagent/config/benchmarks/swebench.yaml) they use) against the [SWE-bench](https://huggingface.co/datasets/princeton-nlp/SWE-bench) dataset of coding problems - 2,294 real-world examples pulled from 12 open source repos: [django/django](https://github.com/django/django) (850), [sympy/sympy](https://github.com/sympy/sympy) (386), [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) (229), [sphinx-doc/sphinx](https://github.com/sphinx-doc/sphinx) (187), [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) (184), [pytest-dev/pytest](https://github.com/pytest-dev/pytest) (119), [pydata/xarray](https://github.com/pydata/xarray) (110), [astropy/astropy](https://github.com/astropy/astropy) (95), [pylint-dev/pylint](https://github.com/pylint-dev/pylint) (57), [psf/requests](https://github.com/psf/requests) (44), [mwaskom/seaborn](https://github.com/mwaskom/seaborn) (22), [pallets/flask](https://github.com/pallets/flask) (11).

这次的新结果是针对他们的"Bash Only"（仅Bash）基准测试，该测试使用他们的 [mini-swe-bench](https://github.com/SWE-agent/mini-swe-agent) 智能体（约9,000行Python代码，[这是他们使用的提示词](https://github.com/SWE-agent/mini-swe-agent/blob/v2.2.1/src/minisweagent/config/benchmarks/swebench.yaml)）在 [SWE-bench](https://huggingface.co/datasets/princeton-nlp/SWE-bench) 编码问题数据集上运行——包含2,294个真实世界示例，来自12个开源代码仓库：[django/django](https://github.com/django/django) (850个)、[sympy/sympy](https://github.com/sympy/sympy) (386个)、[scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) (229个)、[sphinx-doc/sphinx](https://github.com/sphinx-doc/sphinx) (187个)、[matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) (184个)、[pytest-dev/pytest](https://github.com/pytest-dev/pytest) (119个)、[pydata/xarray](https://github.com/pydata/xarray) (110个)、[astropy/astropy](https://github.com/astropy/astropy) (95个)、[pylint-dev/pylint](https://github.com/pylint-dev/pylint) (57个)、[psf/requests](https://github.com/psf/requests) (44个)、[mwaskom/seaborn](https://github.com/mwaskom/seaborn) (22个)、[pallets/flask](https://github.com/pallets/flask) (11个)。

Correction: The Bash only benchmark runs against SWE-bench Verified, not original SWE-bench. Verified is a manually curated subset of 500 samples [described here](https://openai.com/index/introducing-swe-bench-verified/), funded by OpenAI. Here's [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) on Hugging Face - since it's just 2.1MB of Parquet it's easy to browse [using Datasette Lite](https://lite.datasette.io/?parquet=https%3A%2F%2Fhuggingface.co%2Fdatasets%2Fprinceton-nlp%2FSWE-bench_Verified%2Fresolve%2Fmain%2Fdata%2Ftest-00000-of-00001.parquet#/data/test-00000-of-00001?_facet=repo), which cuts those numbers down to django/django (231), sympy/sympy (75), sphinx-doc/sphinx (44), matplotlib/matplotlib (34), scikit-learn/scikit-learn (32), astropy/astropy (22), pydata/xarray (22), pytest-dev/pytest (19), pylint-dev/pylint (10), psf/requests (8), mwaskom/seaborn (2), pallets/flask (1).

更正："Bash Only"基准测试实际上是在 SWE-bench Verified 上运行的，而非原始 SWE-bench。Verified 是一个人工筛选的500样本子集，[详细介绍见此](https://openai.com/index/introducing-swe-bench-verified/)，由 OpenAI 资助。这是 [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) 在 Hugging Face 上的链接——由于它只有2.1MB的 Parquet 文件，使用 [Datasette Lite](https://lite.datasette.io/?parquet=https%3A%2F%2Fhuggingface.co%2Fdatasets%2Fprinceton-nlp%2FSWE-bench_Verified%2Fresolve%2Fmain%2Fdata%2Ftest-00000-of-00001.parquet#/data/test-00000-of-00001?_facet=repo) 很容易浏览，这样样本数量就缩减为：django/django (231个)、sympy/sympy (75个)、sphinx-doc/sphinx (44个)、matplotlib/matplotlib (34个)、scikit-learn/scikit-learn (32个)、astropy/astropy (22个)、pydata/xarray (22个)、pytest-dev/pytest (19个)、pylint-dev/pylint (10个)、psf/requests (8个)、mwaskom/seaborn (2个)、pallets/flask (1个)。

Here's how the top ten models performed:

以下是前十名模型的表现：

It's interesting to see Claude Opus 4.5 beat Opus 4.6, though only by about a percentage point. 4.5 Opus is top, then Gemini 3 Flash, then MiniMax M2.5 - a 229B model released [last week](https://www.minimax.io/news/minimax-m25) by Chinese lab MiniMax. GLM-5, Kimi K2.5 and DeepSeek V3.2 are three more Chinese models that make the top ten as well.

有趣的是，Claude Opus 4.5 以约一个百分点的优势击败了 Opus 4.6。排名首位的是 4.5 Opus，其次是 Gemini 3 Flash，然后是 MiniMax M2.5——这是中国实验室 MiniMax [上周](https://www.minimax.io/news/minimax-m25)发布的229B参数模型。GLM-5、Kimi K2.5 和 DeepSeek V3.2 也跻身前十，是另外三款中国模型。

OpenAI's GPT-5.2 is their highest performing model at position 6, but it's worth noting that their best coding model, GPT-5.3-Codex, is not represented - maybe because it's not yet available in the OpenAI API.

OpenAI 的 GPT-5.2 是他们排名最高的模型，位居第6，但值得注意的是，他们最好的编程模型 GPT-5.3-Codex 并未出现在榜单上——可能是因为它尚未在 OpenAI API 中开放。

This benchmark uses the same system prompt for every model, which is important for a fair comparison but does mean that the quality of the different harnesses or optimized prompts is not being measured here.

这个基准测试对每个模型使用相同的系统提示词，这对公平比较很重要，但这也意味着不同框架（harness）或优化提示词的质量并未在此次测试中得到衡量。

The chart above is a screenshot from the SWE-bench website, but their charts don't include the actual percentage values visible on the bars. I successfully used Claude for Chrome to add these - [transcript here](https://claude.ai/share/81a0c519-c727-4caa-b0d4-0d866375d0da). My prompt sequence included:

上面的图表来自 SWE-bench 网站的截图，但他们的图表并没有在柱状图上显示具体的百分比数值。我成功使用 Claude for Chrome 添加了这个功能——[对话记录在此](https://claude.ai/share/81a0c519-c727-4caa-b0d4-0d866375d0da)。我的提示序列包括：

> Use claude in chrome to open https://www.swebench.com/
> 
> 使用 Chrome 中的 Claude 打开 https://www.swebench.com/
> 
> Click on "Compare results" and then select "Select top 10"
> 
> 点击"Compare results"，然后选择"Select top 10"
> 
> See those bar charts? I want them to display the percentage on each bar so I can take a better screenshot, modify the page like that
> 
> 看到那些柱状图了吗？我希望它们能在每个柱子上显示百分比，这样我就能截一张更好的图了，请修改页面实现这个功能

I'm impressed at how well this worked - Claude injected custom JavaScript into the page to draw additional labels on top of the existing chart.

我对这种方法的效果印象深刻——Claude 向页面注入了自定义 JavaScript，在现有图表上绘制了额外的标签。

Update: If you look at the transcript Claude claims to have switched to Playwright, which is confusing because I didn't think I had that configured.

更新：如果你查看对话记录，Claude 声称切换到了 Playwright，这让我感到困惑，因为我并没有配置过这个工具。

---

## Critical Thinking Commentary / 批判性思考评论

### 作者的核心论点分析

Simon Willison 在本文中提出了几个值得关注的观点：首先，他强调了**第三方独立评估的重要性**——与实验室自行发布的基准测试结果相比，由 SWE-bench 官方进行的独立测试更具可信度。这一观点触及了当前 AI 领域的一个核心问题："自证"式基准测试的偏见风险。当模型开发者自己选择如何报告结果时，存在选择性披露和优化测试条件的可能性。

其次，作者敏锐地观察到**中国 AI 实验室的崛起**——前十名中有一半（MiniMax M2.5、GLM-5、Kimi K2.5、DeepSeek V3.2）来自中国。这一现象不仅反映了技术实力的转移，更暗示了全球 AI 竞争格局正在发生深刻变化。值得注意的是，作者并未简单罗列排名，而是指出了排名背后的有趣细节：Claude Opus 4.5 反而击败了更新的 4.6 版本。

第三，作者对**基准测试局限性的清醒认识**——他明确指出，使用相同系统提示词虽然保证了公平比较，但也意味着没有衡量不同框架或优化提示词的质量。这种自我反思的态度在 AI 报道中并不常见。

### 文章的优势与不足

**优势：**

1. **数据来源透明**：作者不仅提供了原始链接，还详细说明了数据集的构成和来源，包括更正说明（从原始 SWE-bench 到 SWE-bench Verified 的修正），这种严谨的态度增强了文章的可信度。

2. **实用价值高**：通过 Claude for Chrome 修改图表添加百分比的具体案例，展示了 AI 辅助工具在数据可视化中的实际应用，这部分内容为读者提供了可操作的方法论。

3. **国际视野**：对中国模型的关注体现了作者的开阔视野，避免了以美国为中心的偏见。

**不足：**

1. **缺乏深入分析**：文章主要停留在事实陈述层面，对排名结果的深层含义探讨不足。例如，为什么中国模型能在代码任务上表现突出？这反映了什么样的技术路线差异？

2. **样本代表性存疑**：SWE-bench Verified 只有 500 个样本，且主要来自 Python 项目。作者虽然提到了这一点，但未深入讨论这种局限性对结果的普适性影响。

3. **对 OpenAI 缺席的推测过于保守**：作者猜测 GPT-5.3-Codex 未上榜是因为尚未在 API 中开放，但未探讨其他可能性，例如该模型在 SWE-bench 上表现不佳、或 OpenAI 有意避免参与此类直接对比等。

### 我的批判性视角

**关于基准测试本身的反思：**

SWE-bench 测量的是模型在受控环境中解决已知问题的能力，但这与实际软件工程工作存在本质差异。真实的开发场景涉及模糊需求、遗留代码、团队协作、时间压力等复杂因素。一个模型能在 SWE-bench 上获得高分，并不意味着它能成为优秀的"AI 软件工程师"。我们可能在过度优化一个不完全反映现实需求的指标。

**关于中国模型崛起的深层解读：**

文章将中国模型的成功简单归因于技术实力，但我认为背后可能存在其他因素：
- **数据偏见**：SWE-bench 基于开源 Python 项目，而这些项目中的很多代码注释和 issue 讨论都是英文的。中国模型可能在训练数据上对这些特定领域进行了更有针对性的优化。
- **评估方式的影响**："Bash Only"测试环境可能更适合某些模型的架构特点。
- **资源集中效应**：中国实验室可能在特定基准测试上投入更多优化资源，以在国际竞争中获得知名度。

**关于 Claude for Chrome 案例的再思考：**

作者将此作为成功案例分享，但我看到的是一个潜在的警示信号：当 AI 工具能够如此容易地修改网页内容时，我们如何确保所见即所得？虽然在这个案例中修改是善意的（添加百分比），但这种能力也可能被用于误导性目的。此外，作者对 Claude "声称切换到 Playwright"表示困惑，这暗示了当前 AI 工具的行为可解释性仍然不足。

### 延伸影响与思考

1. **基准测试的军备竞赛风险**：随着模型在 SWE-bench 等标准测试上接近饱和（前几名差距仅在 1-2 个百分点），我们可能需要重新思考如何评估 AI 能力。是否应转向更动态、更难以"刷分"的评估方式？

2. **地缘政治与技术标准**：中国模型在 SWE-bench 上的强势表现可能促使西方实验室重新评估合作与竞争策略。技术基准测试正在成为软实力的竞技场。

3. **AI 辅助内容创作的双重性**：作者使用 Claude 改进图表的经历展示了人机协作的潜力，但也引发了关于"AI 中介现实"的思考——当我们越来越多地通过 AI 滤镜观察世界时，原始信息可能变得难以辨认。

4. **开放与封闭的权衡**：SWE-bench 作为开放基准测试的成功，与 OpenAI 可能选择不参与的行为形成对比。这种"开放 vs 封闭"的张力将定义 AI 发展的下一阶段。
