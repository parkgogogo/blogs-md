# SWE-bench 2026年2月排行榜更新

**原文链接**: https://simonwillison.net/2026/Feb/19/swe-bench/

**标签**: `SWE-bench`, `AI基准测试`, `代码生成`, `大语言模型`, `Claude`, `GPT`, `Gemini`, `DeepSeek`

---

## 正文

[SWE-bench 2026年2月排行榜更新](https://www.swebench.com/)（[来源](https://twitter.com/KLieret/status/2024176335782826336)）

SWE-bench 是各大实验室在发布模型时都喜欢引用的基准测试之一。官方排行榜更新频率不高，但他们刚刚针对当前这一代模型进行了一次完整测试，这值得关注——因为能看到这种并非由实验室自行报告的基准测试结果总是好事。

这次的新结果是针对他们的"Bash Only"（仅Bash）基准测试，该测试使用他们的 [mini-swe-bench](https://github.com/SWE-agent/mini-swe-agent) 智能体（约9,000行Python代码，[这是他们使用的提示词](https://github.com/SWE-agent/mini-swe-agent/blob/v2.2.1/src/minisweagent/config/benchmarks/swebench.yaml)）在 [SWE-bench](https://huggingface.co/datasets/princeton-nlp/SWE-bench) 编码问题数据集上运行——包含2,294个真实世界示例，来自12个开源代码仓库：[django/django](https://github.com/django/django) (850个)、[sympy/sympy](https://github.com/sympy/sympy) (386个)、[scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) (229个)、[sphinx-doc/sphinx](https://github.com/sphinx-doc/sphinx) (187个)、[matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) (184个)、[pytest-dev/pytest](https://github.com/pytest-dev/pytest) (119个)、[pydata/xarray](https://github.com/pydata/xarray) (110个)、[astropy/astropy](https://github.com/astropy/astropy) (95个)、[pylint-dev/pylint](https://github.com/pylint-dev/pylint) (57个)、[psf/requests](https://github.com/psf/requests) (44个)、[mwaskom/seaborn](https://github.com/mwaskom/seaborn) (22个)、[pallets/flask](https://github.com/pallets/flask) (11个)。

**更正**："Bash Only"基准测试实际上是在 SWE-bench Verified 上运行的，而非原始 SWE-bench。Verified 是一个人工筛选的500样本子集，[详细介绍见此](https://openai.com/index/introducing-swe-bench-verified/)，由 OpenAI 资助。这是 [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) 在 Hugging Face 上的链接——由于它只有2.1MB的 Parquet 文件，使用 [Datasette Lite](https://lite.datasette.io/?parquet=https%3A%2F%2Fhuggingface.co%2Fdatasets%2Fprinceton-nlp%2FSWE-bench_Verified%2Fresolve%2Fmain%2Fdata%2Ftest-00000-of-00001.parquet#/data/test-00000-of-00001?_facet=repo) 很容易浏览，这样样本数量就缩减为：django/django (231个)、sympy/sympy (75个)、sphinx-doc/sphinx (44个)、matplotlib/matplotlib (34个)、scikit-learn/scikit-learn (32个)、astropy/astropy (22个)、pydata/xarray (22个)、pytest-dev/pytest (19个)、pylint-dev/pylint (10个)、psf/requests (8个)、mwaskom/seaborn (2个)、pallets/flask (1个)。

以下是前十名模型的表现：

有趣的是，Claude Opus 4.5 以约一个百分点的优势击败了 Opus 4.6。排名首位的是 4.5 Opus，其次是 Gemini 3 Flash，然后是 MiniMax M2.5——这是中国实验室 MiniMax [上周](https://www.minimax.io/news/minimax-m25)发布的229B参数模型。GLM-5、Kimi K2.5 和 DeepSeek V3.2 也跻身前十，是另外三款中国模型。

OpenAI 的 GPT-5.2 是他们排名最高的模型，位居第6，但值得注意的是，他们最好的编程模型 GPT-5.3-Codex 并未出现在榜单上——可能是因为它尚未在 OpenAI API 中开放。

这个基准测试对每个模型使用相同的系统提示词，这对公平比较很重要，但这也意味着不同框架（harness）或优化提示词的质量并未在此次测试中得到衡量。

上面的图表来自 SWE-bench 网站的截图，但他们的图表并没有在柱状图上显示具体的百分比数值。我成功使用 Claude for Chrome 添加了这个功能——[对话记录在此](https://claude.ai/share/81a0c519-c727-4caa-b0d4-0d866375d0da)。我的提示序列包括：

> 使用 Chrome 中的 Claude 打开 https://www.swbeech.com/
> 
> 点击"Compare results"，然后选择"Select top 10"
> 
> 看到那些柱状图了吗？我希望它们能在每个柱子上显示百分比，这样我就能截一张更好的图了，请修改页面实现这个功能

我对这种方法的效果印象深刻——Claude 向页面注入了自定义 JavaScript，在现有图表上绘制了额外的标签。

**更新**：如果你查看对话记录，Claude 声称切换到了 Playwright，这让我感到困惑，因为我并没有配置过这个工具。

---

*翻译说明：本文介绍了2026年2月SWE-bench排行榜的更新情况，重点分析了各大AI模型在软件工程任务上的表现。值得注意的是，本次测试采用了第三方独立评估的方式，而非实验室自行报告的结果，增加了数据的可信度。同时，多款中国模型（MiniMax M2.5、GLM-5、Kimi K2.5、DeepSeek V3.2）进入前十，显示了中国AI在该领域的竞争力。*
