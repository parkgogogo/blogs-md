# Thoughts on AI Progress (Dec 2025)

**Author:** Dwarkesh Patel  
**Published:** December 2, 2025  
**Original URL:** https://www.dwarkesh.com/p/thoughts-on-ai-progress-dec-2025

---

I'm confused why some people have short timelines and at the same time are bullish on the current scale up of reinforcement learning atop LLMs. If we're actually close to a human-like learner, this whole approach of training on verifiable outcomes is doomed.

我感到困惑的是，为什么有些人既认为 AGI 即将到来（短期时间线），又对当前基于大语言模型的强化学习规模扩展持乐观态度。如果我们真的接近类人类的学习者，那么这种基于可验证结果进行训练的整体方法注定是失败的。

Currently the labs are trying to bake in a bunch of skills into these models through "mid-training" - there's an entire supply chain of companies building RL environments which teach the model how to navigate a web browser or use Excel to write financial models.

目前，实验室正试图通过"中期训练"将一系列技能植入这些模型——整个供应链的公司都在构建强化学习环境，教模型如何浏览网页或使用 Excel 编写财务模型。

Either these models will soon learn on the job in a self directed way - making all this pre-baking pointless - or they won't - which means AGI is not imminent. Humans don't have to go through a special training phase where they need to rehearse every single piece of software they might ever need to use.

要么这些模型很快就能以自主方式在工作中学习——这使得所有这些预训练变得毫无意义——要么它们做不到——这意味着 AGI 并非迫在眉睫。人类不需要经历一个特殊的训练阶段，去演练他们可能需要的每一个软件。

Beren Millidge made interesting points about this in a recent blog post:

> When we see frontier models improving at various benchmarks we should think not just of increased scale and clever ML research ideas but billions of dollars spent paying PhDs, MDs, and other experts to write questions and provide example answers and reasoning targeting these precise capabilities ... In a way, this is like a large-scale reprise of the expert systems era, where instead of paying experts to directly program their thinking as code, they provide numerous examples of their reasoning and process formalized and tracked, and then we distill this into models through behavioural cloning. This has updated me slightly towards longer AI timelines since given we need such effort to design extremely high quality human trajectories and environments for frontier systems implies that they still lack the critical core of learning that an actual AGI must possess.

Beren Millidge 在最近的一篇博客文章中提出了有趣的观点：

> 当我们看到前沿模型在各种基准测试上取得进步时，我们不应该只想到规模增加和巧妙的机器学习研究想法，还应该想到花费数十亿美元聘请博士、医生和其他专家来编写问题并提供针对这些精确能力的示例答案和推理……在某种程度上，这就像是专家系统时代的大规模重演，只不过我们不是付钱给专家让他们将思维直接编程为代码，而是让他们提供大量推理示例和经过形式化及追踪的流程，然后我们通过行为克隆将这些提炼成模型。这让我对 AI 时间线的预期稍微延长了一些，因为既然我们需要如此大量的努力来为前沿系统设计极高质量的人类轨迹和环境，这意味着它们仍然缺乏真正的 AGI 必须具备的关键学习核心。

You can see this tension most vividly in robotics. In some fundamental sense, robotics is an algorithms problem, not a hardware or data problem — with very little training, humans can learn how to teleoperate current hardware to do useful work. So if we had a human like learner, robotics would (in large part) be solved. But the fact that we don't have such a learner makes it necessary to go out into a thousand different homes to learn how to pick up dishes or fold laundry.

在机器人领域，你可以最生动地看到这种张力。从某种根本意义上说，机器人是一个算法问题，而不是硬件或数据问题——人类只需很少的训练就能学会如何远程操作当前的硬件来完成有用的工作。所以如果我们有一个类人类的学习者，机器人问题（在很大程度上）就已经解决了。但事实上我们没有这样的学习者，这就使得有必要进入一千个不同的家庭去学习如何收拾盘子或叠衣服。

One counterargument I've heard from the takeoff-within-5-years crew is that we have to do this cludgy RL in service of building a superhuman AI researcher, and then the million copies of automated Ilya can go figure out how to solve robust and efficient learning from experience.

我听到过来自"5 年内起飞派"的一个反驳是：我们必须进行这种笨拙的强化学习，是为了构建一个超人类的 AI 研究员，然后数以百万计的自动化 Ilya（指 OpenAI 首席科学家 Ilya Sutskever）副本可以去研究如何从经验中进行稳健而高效的学习。

This gives the vibes of that old joke, "We're losing money on every sale, but we'll make it up in volume." Somehow this automated researcher is going to figure out the algorithm for AGI - a problem humans have been banging their head against for the better part of a century - while not having the basic learning capabilities that children have? I find this super implausible.

这让我想起那个老笑话的 vibe："我们每笔销售都在亏钱，但我们会靠销量来弥补。"不知怎的，这个自动化研究员将要破解 AGI 的算法——这是人类近一个世纪以来一直在绞尽脑汁解决的问题——而它却不具备儿童拥有的基本学习能力？我觉得这非常不可信。

Besides, even if you think the RLVR scaleup will soon help us automate AI research, the labs' actions suggest otherwise. You don't need to pre-bake the consultant's skills at crafting Powerpoint slides in order to automate Ilya. So clearly the labs' actions hint at a world view where these models will continue to fare poorly at generalizing and on-the-job learning, thus making it necessary to build in the skills that they hope will be economically valuable.

此外，即使你认为 RLVR（可验证奖励强化学习）的规模扩展很快就能帮助我们自动化 AI 研究，实验室的行为却暗示了相反的情况。你不需要预先训练咨询师制作 PowerPoint 幻灯片的技能来自动化 Ilya 的工作。所以很明显，实验室的行为暗示了一种世界观：这些模型在泛化和在职学习方面将继续表现不佳，因此有必要预先植入他们希望具有经济价值的技能。

Another counterargument you could make is that even if the model could learn these skills on the job, it is just so much more efficient to build them up just once during training rather that again and again for each user or company. And look, it makes a lot of sense to just bake in fluency with common tools like browsers and terminals. Indeed one of the key advantages that AGIs will have is this greater capacity to share knowledge across copies. But people are underrating how much company and context specific skills are required to do most jobs. And there just isn't currently a robust efficient way for AIs to pick up those skills.

你可以提出的另一个反驳是，即使模型可以在工作中学习这些技能，在训练期间一次性建立这些技能比为每个用户或公司反复训练要高效得多。而且，将浏览器和终端等常用工具的熟练度直接植入模型是说得通的。事实上，AGI 的关键优势之一就是跨副本共享知识的能力更强。但人们低估了完成大多数工作所需的公司特定和上下文特定技能的数量。而目前 AI 还没有一种稳健高效的方法来掌握这些技能。

I was at a dinner with an AI researcher and a biologist. The biologist said she had long timelines. We asked what she thought AI would struggle with. She said her work has recently involved looking at slides and decide if a dot is actually a macrophage or just looks like one. The AI researcher says, "Image classification is a textbook deep learning problem—we could easily train for that."

我曾经和一位 AI 研究员以及一位生物学家共进晚餐。生物学家说她认为 AGI 需要很长时间才能实现。我们问她认为 AI 会在什么方面遇到困难。她说她的工作最近涉及查看载玻片，判断一个斑点究竟是巨噬细胞还是只是看起来像。AI 研究员说："图像分类是教科书级别的深度学习问题——我们可以轻松训练出这种能力。"

I thought this was a very interesting exchange, because it revealed a key crux between me and the people who expect transformative economic impacts in the next few years. Human workers are valuable precisely because we don't need to build schleppy training loops for every small part of their job. It's not net-productive to build a custom training pipeline to identify what macrophages look like given the way this particular lab prepares slides, then another for the next lab-specific micro-task, and so on. What you actually need is an AI that can learn from semantic feedback or from self directed experience, and then generalize, the way a human does.

我认为这是一次非常有趣的交流，因为它揭示了我和那些期待未来几年产生变革性经济影响的人之间的关键分歧。人类工人之所以有价值，恰恰是因为我们不需要为他们工作的每一个小部分构建繁琐的训练循环。为这个特定实验室制备载玻片的方式构建一个自定义训练管道来识别巨噬细胞的样子，然后再为下一个实验室特定的微观任务构建另一个，如此往复，这不是净生产力的做法。你真正需要的是一种能够从语义反馈或自我指导经验中学习，然后像人类一样进行泛化的 AI。

Every day, you have to do a hundred things that require judgment, situational awareness, and skills & context learned on the job. These tasks differ not just across different people, but from one day to the next even for the same person. It is not possible to automate even a single job by just baking in some predefined set of skills, let alone all the jobs.

每一天，你都必须做一百件需要判断力、情境意识以及在工作中学习的技能和上下文的事情。这些任务不仅在不同的人之间有所不同，即使对同一个人来说，每天也不尽相同。仅仅通过植入一些预定义的技能集是不可能自动化哪怕一个工作的，更不用说所有工作了。

In fact, I think people are really underestimating how big a deal actual AGI will be because they're just imagining more of this current regime. They're not thinking about billions of human-like intelligences on a server which can copy and merge all their learnings. And to be clear, I expect this (aka actual AGI) in the next decade or two. That's fucking crazy!

事实上，我认为人们真的低估了真正的 AGI 会有多重要，因为他们只是在想象更多当前的模式。他们没有考虑到服务器上数十亿个类人智能可以复制和合并它们所有的学习成果。明确地说，我预计这（即真正的 AGI）将在未来一二十年内实现。这太疯狂了！

Sometimes people will say that the reason that AIs aren't more widely deployed across firms and already providing lots of value (outside of coding) is that technology takes a long time to diffuse. I think this is cope. People are using this cope to gloss over the fact that these models just lack the capabilities necessary for broad economic value.

有时人们会说，AI 没有在企业中更广泛部署并已经提供大量价值（除了编程之外）的原因是技术扩散需要时间。我认为这是一种自我安慰。人们用这种自我安慰来掩盖这些模型只是缺乏广泛经济价值所需能力的事实。

Steven Byrnes has an excellent post on this and many other points:

> New technologies take a long time to integrate into the economy? Well ask yourself: how do highly-skilled, experienced, and entrepreneurial immigrant humans manage to integrate into the economy immediately? Once you've answered that question, note that AGI will be able to do those things too.

Steven Byrnes 就这一点和许多其他观点写了一篇出色的文章：

> 新技术需要很长时间才能融入经济？那请问：高技能、经验丰富且具有创业精神的移民人类是如何立即融入经济的？一旦你回答了这个问题，请注意 AGI 也能做这些事情。

If these models were actually like humans on a server, they'd diffuse incredibly quickly. In fact, they'd be so much easier to integrate and onboard than a normal human employee (they could read your entire Slack and Drive in minutes and immediately distill all the skills your other AI employees have). Plus, hiring is very much like a lemons market, where it's hard to tell who the good people are, and hiring someone bad is quite costly. This is a dynamic you wouldn't have to worry about when you just wanna spin up another instance of a vetted AGI model.

如果这些模型真的像服务器上的人类，它们会扩散得非常快。事实上，它们会比普通人类员工更容易整合和入职（它们可以在几分钟内阅读你的整个 Slack 和 Drive，并立即提炼出你的其他 AI 员工拥有的所有技能）。此外，雇佣非常像一个柠檬市场（次品市场），很难分辨谁是好人，雇错人的成本相当高。而当你只是想启动另一个经过验证的 AGI 模型实例时，你不必担心这种动态。

For these reasons, I expect it's going to be much much easier to diffuse AI labor into firms than it is to hire a person. And companies hire lots of people all the time. If the capabilities were actually at AGI level, people would be willing to spend trillions of dollars a year buying tokens (knowledge workers cumulatively earn 10s of trillions of dollars of wages a year). The reason that lab revenue are 4 orders of magnitude off right now is that the models are nowhere near as capable as human knowledge workers.

出于这些原因，我预计将 AI 劳动力扩散到企业中会比雇佣一个人容易得多。而公司一直都在大量雇佣人员。如果能力真的达到了 AGI 水平，人们愿意每年花费数万亿美元购买 token（知识工作者每年累计赚取数十万亿美元的工资）。实验室收入目前相差 4 个数量级的原因是，这些模型的能力远远不及人类知识工作者。

AI bulls will often criticize AI bears for repeatedly moving the goal posts. This is often fair. AI has made a ton of progress in the last decade, and it's easy to forget that.

AI 乐观派经常批评 AI 悲观派反复移动目标柱。这通常是公平的。AI 在过去十年取得了巨大进步，人们很容易忘记这一点。

But some amount of goal post shifting is justified. If you showed me Gemini 3 in 2020, I would have been certain that it could automate half of knowledge work. We keep solving what we thought were the sufficient bottlenecks to AGI (general understanding, few shot learning, reasoning), and yet we still don't have AGI (defined as, say, being able to completely automate 95% of knowledge work jobs). What is the rational response?

但一定程度的目标柱移动是合理的。如果你在 2020 年给我展示 Gemini 3，我肯定会确定它能自动化一半的知识工作。我们不断解决了我们认为通往 AGI 的充分瓶颈（通用理解、少样本学习、推理），但我们仍然没有 AGI（定义为能够完全自动化 95% 的知识工作）。理性的回应是什么？

It's totally reasonable to look at this and say, "Oh actually there's more to intelligence and labor than I previously realized. And while we're really close to (and in many ways have surpassed) what I would have defined as AGI in the past, the fact that model companies are not making trillions is revenue clearly reveals that my previous definition of AGI was too narrow."

看着这一切并说"哦，实际上智能和劳动比我之前意识到的要复杂得多"是完全合理的。虽然我们真的很接近（并在许多方面已经超越了）我过去定义的 AGI，但模型公司没有赚取数万亿美元收入这一事实清楚地表明，我之前对 AGI 的定义过于狭隘。

I expect this to keep happening into the future. I expect that by 2030 that the labs will have made significant progress on my hobby horse of continual learning, and the models will start earning 100s of billions in revenue, but they won't have automated all knowledge work, and I'll be like, "We've made a lot of progress, but we're not at AGI yet. We also need X, Y, and Z thing to get to trillions in revenue."

我预计这种情况在未来会继续发生。我预计到 2030 年，实验室将在持续学习（这是我的执念）方面取得重大进展，模型将开始赚取数千亿美元的收入，但它们不会自动化所有知识工作，而我会说："我们取得了很大进步，但我们还没有达到 AGI。我们还需要 X、Y 和 Z 才能达到数万亿美元的收入。"

Models keep getting more impressive at the rate the short timelines people predict, but more useful at the rate the long timelines people predict.

模型在以短期时间线预测者预测的速度变得越来越令人印象深刻，但只在以长期时间线预测者预测的速度变得越来越有用。

With pretraining, we had this extremely clean and general trend in improvement in loss across multiple orders of magnitude of compute (albeit on a power law, which is as weak as exponential growth is strong). People are trying to launder the prestige of pretraining scaling, which was almost as predictable as宇宙物理定律, to justify bullish projections about RLVR, for which we have no well fit publicly known trend. When intrepid researchers do try to piece together the implications from稀缺的公开数据点, they get quite bearish results. For example, Toby Ord has a great post where he cleverly connects the dots between different o-series benchmark charts, which suggested "we need something like a 1,000,000x scale-up of total RL compute to give a boost similar to a GPT level".

在预训练方面，我们有一个极其清晰和普遍的趋势，即损失在多个数量级的计算量上持续改善（虽然是幂律，它的弱度与指数增长的强度相当）。人们试图利用预训练扩展的声望——这几乎像物理定律一样可预测——来为 RLVR 的乐观预测辩护，而我们对后者没有良好拟合的公开趋势。当勇敢的研究人员试图从稀缺的公开数据点拼凑含义时，他们得到了相当悲观的结果。例如，Toby Ord 有一篇很棒的帖子，他巧妙地将不同的 o 系列基准图表联系起来，表明"我们需要将 RL 计算总量扩展大约 100 万倍，才能获得类似于 GPT 级别的提升"。

There is huge variance in the amount of value that different humans can add, especially in white collar with its O-ring dynamics. The village idiot adds ~0 value to knowledge work, while top AI researchers are worth billions of dollars to Mark Zuckerberg.

不同人类能够增加的价值存在巨大差异，尤其是在白领工作中，具有 O-ring 动态（一环失误全盘皆输）。乡村傻瓜对知识工作的贡献约为 0，而顶级 AI 研究员对马克·扎克伯格来说价值数十亿美元。

AI models at any given snapshot of time, however, are roughly equally capable. Humans have all this variance, whereas AI models don't. Because a disproportionate share of value-add in knowledge work comes from the top percentile humans, if we try to compare the intelligence of these AI models to the median human, then we will systematically overestimate the value they can generate. But by the same token, when models finally do match top human performance, their impact might be quite explosive.

然而，在任何给定的时间快照中，AI 模型的能力大致相同。人类有这么多差异，而 AI 模型没有。因为知识工作中不成比例的价值增值来自顶尖百分位的人类，如果我们试图将这些 AI 模型的智能与中位数人类相比，那么我们会系统性地高估它们能产生的价值。但同样地，当模型最终确实匹配顶尖人类表现时，它们的影响可能相当爆炸性。

People have spent a lot of time talking about a software only singularity (where AI models write the code for a smarter successor system), a software + hardware singularity (where AIs also improve their successor's computing hardware), or variations therein.

人们花了很多时间讨论纯软件奇点（AI 模型为更聪明的后继系统编写代码）、软件+硬件奇点（AI 还改进其后继者的计算硬件）或其变体。

All these scenarios neglect what I think will be the main driver of further improvements atop AGI: continual learning. Again, think about how humans become more capable at anything. It's mostly from experience in the relevant domain.

所有这些情景都忽视了我认为是 AGI 之上进一步改进的主要驱动力：持续学习。再说一次，想想人类是如何在任何事上变得更擅长的。这主要来自于相关领域的经验。

Over conversation, Beren Millidge made the interesting suggestion that the future might look continual learning agents going out, doing jobs and generating value, and then bringing all their learnings back to the hive mind model, which does some kind of batch distillations on all these agents. The agents themselves could be quite specialized - containing what Karpathy called "the cognitive core" plus knowledge and skills relevant to the job they're being deployed to do.

在谈话中，Beren Millidge 提出了一个有趣的建议：未来可能会是持续学习智能体外出工作、创造价值，然后将所有学习成果带回蜂巢思维模型，后者对所有这些智能体进行某种批处理蒸馏。智能体本身可能相当专业化——包含 Karpathy 所说的"认知核心"加上与它们被部署去做的工作相关的知识和技能。

"Solving" continual learning won't be a singular one-and-done achievement. Instead, it will feel like solving in context learning. GPT-3 demonstrated that in context learning could be very powerful (its ICL capabilities were so remarkable that the title of the GPT-3 paper is 'Language Models are Few-Shot Learners'). But of course, we didn't "solve" in-context learning when GPT-3 came out - and indeed there's plenty of progress still to be made, from comprehension to context length. I expect a similar progression with continual learning. Labs will probably release something next year which they call continual learning, and which will in fact count as progress towards continual learning. But human level continual learning may take another 5 to 10 years of further progress.

"解决"持续学习不会是一个一次性完成的单一成就。相反，它会感觉像是解决上下文学习。GPT-3 证明了上下文学习可以非常强大（它的 ICL 能力如此显著，以至于 GPT-3 论文的标题是《语言模型是少样本学习者》）。但当然，GPT-3 问世时我们并没有"解决"上下文学习——事实上，从理解能力到上下文长度，仍有大量进步要做。我预计持续学习也会有类似的进展。实验室可能会明年发布某种他们称之为持续学习的东西，而且这确实会被视为持续学习的进步。但人类水平的持续学习可能还需要再过 5 到 10 年的进一步进步。

This is why I don't expect some kind of runaway gains to the first model that cracks continual learning, thus getting more and more widely deployed and capable. If you had fully solved continual learning drop out of nowhere, then sure, it's "game set match", as Satya put it. But that's not what's going to happen. Instead, some lab is going to figure out how to get some initial traction on the problem. Playing around with this feature will make it clear how it was implemented, and the other labs will soon replicate this breakthrough and稍微改进一下。

这就是为什么我不期望第一个破解持续学习的模型会产生某种失控的收益，从而被越来越广泛地部署和变得更强大。如果你突然完全解决了持续学习，那么当然，就像 Satya 说的，"比赛结束了"。但这不是将要发生的事。相反，某个实验室会想出如何在这个问题上获得初步进展。玩弄这个功能会让人清楚它是如何实现的，其他实验室很快就会复制这一突破并稍微改进。

There'll also probably be diminishing returns from learning-from-deployment. Each of the first 1000 consultant agents are each learning a ton from deployment. Less so the next 1000. And is there such a long tail to consultant work that the millionth deployed instance is likely to see something super important the other 999,999 instances missed? In fact, I wouldn't be surprised if continual learning also ends up leading to a power law, but with respect to the number of instances deployed.

从部署中学习的收益递减也很可能发生。前 1000 个咨询师智能体每个都从部署中学到大量东西。接下来的 1000 个就少多了。咨询工作真的有那么长的长尾，以至于第 100 万个部署的实例可能会看到其他 99.9999 万个实例错过的重要东西吗？事实上，如果持续学习最终也导致幂律分布（但相对于部署的实例数量），我也不会感到惊讶。

Besides, I just have some prior that competition will stay fierce, informed by the observation that all these previous supposed flywheels（用户参与度、合成数据等）have done very little to diminish the greater and greater competition between model companies. Every month（或更少）, the big three will rotate around the podium, with other competitors not that far behind. There is some force（可能是人才挖角、谣言工厂或逆向工程）which has so far neutralized any single实验室可能拥有的失控优势。

此外，我只是有一种先验信念，认为竞争将保持激烈，这是基于观察到所有先前所谓的飞轮（用户参与度、合成数据等）对减少模型公司之间日益激烈的竞争几乎没有做什么。每个月（或更少），三大巨头会在领奖台上轮换，其他竞争者也不遑多让。有某种力量（可能是人才挖角、谣言工厂或逆向工程）迄今已中和了任何单一实验室可能拥有的失控优势。

---

## 批判性思考评论

### 1. 作者的核心论点

Dwarkesh Patel 在这篇文章中提出了一个强有力的论证：**当前 AI 进展的瓶颈不在于规模扩展，而在于持续学习能力的缺失**。他指出，如果 AI 真的接近 AGI，那么当前这种"预训练所有技能"的方法应该是多余的——真正的智能应该能像人类一样在工作中自主学习。

### 2. 最有说服力的论据

作者用生物学家的例子非常生动地说明了问题核心：AI 研究员认为图像分类是"教科书级问题"，但生物学家指出每个实验室的样本制备方式都不同，需要针对特定情境的判断力。这揭示了当前 AI 的根本局限：**它缺乏人类那种从语义反馈和自我导向经验中学习的灵活性**。

另一个有力论点是关于经济扩散的。如果 AI 真的像人类一样能干，它应该比人类更容易融入经济（无需招聘筛选、可瞬间复制知识），但现实是实验室收入与人类知识工作者工资相差 4 个数量级。

### 3. 值得商榷的地方

**关于 RLVR 的悲观预测**：作者对 RLVR（可验证奖励强化学习）的悲观态度可能过于绝对。虽然 Toby Ord 的分析显示需要百万倍扩展，但 OpenAI 的 o1/o3 系列已经展现出令人印象深刻的推理能力，且我们尚未看到 RLVR 的极限。

**关于持续学习的悲观时间线**：作者预测人类水平的持续学习还需要 5-10 年，但这可能低估了当前研究的速度。考虑到 2024-2025 年 AI 领域的进展速度，这个预测可能过于保守。

**忽略了涌现的可能性**：作者假设持续学习将是渐进式的改进，但忽视了 AI 能力可能涌现的可能性——某些能力可能在没有预警的情况下突然出现。

### 4. 更深层的思考

这篇文章引发了一个哲学问题：**什么是真正的智能？** 如果 AI 能在所有基准测试上超越人类，但仍然需要为每个具体任务进行专门训练，它算是"通用"智能吗？

作者的答案是：不算。真正的通用智能应该具有**迁移学习和自主适应**的能力。这与图灵测试时代的观点形成了有趣对比——当时我们认为只要 AI 能对话就是智能，而现在标准已经提高到了经济价值创造。

### 5. 对 AI 时间线的影响

这篇文章对 AI 时间线预测有重要影响：
- **短期（1-3 年）**：AI 将继续在特定任务上表现出色，但在需要灵活适应的工作上表现有限
- **中期（5-10 年）**：持续学习可能取得突破，使 AI 能够自动化更多知识工作
- **长期（10 年以上）**：真正的 AGI 可能需要解决持续学习、常识推理和世界模型等多个问题

### 6. 结论

这是一篇深思熟虑的文章，提供了一个重要的视角来评估 AI 进展。**它提醒我们不要被炫目的技术演示所迷惑，而应该关注实际的经济价值和泛化能力**。作者的观点与最近一些 AGI 乐观派的预测形成对比，为这个领域提供了必要的冷静声音。

然而，考虑到 AI 进展的指数性质，作者对持续学习需要 5-10 年的预测可能是保守的。2025 年已经见证了多个突破，包括推理能力的重大进步。或许真正的答案介于短期乐观派和长期悲观派之间——AGI 可能比我们想象的更近，但实现方式可能与当前的主流预期不同。

---

*翻译与评论完成于 2025 年 2 月 25 日*
