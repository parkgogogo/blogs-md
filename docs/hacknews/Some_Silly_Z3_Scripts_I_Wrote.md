URL: https://buttondown.com/hillelwayne/archive/new-blog-post-some-silly-z3-scripts-i-wrote/

Now that I'm not spending all my time on Logic for Programmers, I have time to update my website again! So here's the first blog post in five months: [Some Silly Z3 Scripts I Wrote](https://www.hillelwayne.com/post/z3-examples/).

既然我不再把所有时间都花在《程序员逻辑学》上了，我终于有时间更新我的网站了！这是五个月来的第一篇博客文章：[我写的一些有趣的 Z3 脚本](https://www.hillelwayne.com/post/z3-examples/)。

Normally I'd also put a link to the Patreon notes but I've decided I don't like publishing gated content and am going to wind that whole thing down. So some quick notes about this post:

通常我也会放上 Patreon 笔记的链接，但我决定不喜欢发布付费墙内容，所以打算逐步停止那个项目。关于这篇文章，有几点快速说明：

- Part of the point is admittedly to hype up the eventual release of LfP. I want to start marketing the book, but don't want the marketing material to be devoid of interest, so tangentially-related-but-independent blog posts are a good place to start.

- 部分内容确实是为了宣传《程序员逻辑学》最终发布而造势。我想开始为这本书做营销，但又不希望营销材料毫无趣味性，所以这种与主题相关但又独立成章的博客文章是一个不错的起点。

- The post discusses the concept of "chaff", the enormous quantity of material (both code samples and prose) that didn't make it into the book. The book is about 50,000 words… and considerably shorter than the total volume of chaff! I don't think most of it can be turned into有用的 public posts, but I'm not entirely opposed to the idea. Maybe some of the old chapters could be made into something?

- 这篇文章讨论了"谷壳"的概念——那些未能收入书中的大量材料（包括代码示例和文字）。这本书大约有 5 万字……但比起谷壳的总量来说要短得多！我认为大部分内容可能无法变成有用的公开文章，但我也不完全反对这个想法。也许有些旧章节可以改编成什么内容？

- Coming up with a conditioned mathematical property to prove was a struggle. I had two candidates: a == b * c => a / b == c, which would have required a long tangent on how division must be total in Z3, and a != 0 => some b: b * a == 1, which would have required introducing a quantifier (SMT is real weird about quantifiers). Division by zero has already caused me enough grief so I went with the latter. This did mean I had to reintroduce "operations must be total" when talking about arrays.

- 想出一个需要证明的条件数学性质是一件困难的事。我有两个候选：a == b * c => a / b == c，这需要大段偏离主题来解释除法在 Z3 中必须是全函数的；以及 a != 0 => 存在 b: b * a == 1，这需要引入量词（SMT 对量词的处理非常奇怪）。除零问题已经给我带来够多的麻烦了，所以我选择了后者。但这确实意味着我在讨论数组时必须重新引入"操作必须是全函数"的概念。

- I have no idea why the array example returns 2 for the max profit and not 99999999. I'm guessing there's some short circuiting logic in the optimizer when the problem is ill-defined?

- 我完全不知道为什么数组示例中最大利润返回的是 2 而不是 99999999。我猜测当问题定义不明确时，优化器中可能存在某种短路逻辑？

- One example I could not get working, which is unfortunate, was a demonstration of how SMT solvers are undecidable via encoding Goldbach's conjecture as an SMT problem. Anything with multiple nested quantifiers is a pain.

- 有一个例子我没能成功运行，这很遗憾，那就是通过将哥德巴赫猜想编码为 SMT 问题来展示 SMT 求解器是不可判定的。任何包含多个嵌套量词的东西都很麻烦。

If you're reading this on the web, you can subscribe [here](/hillelwayne). Updates are once a week. My main website is [here](https://www.hillelwayne.com).

如果你在网页上阅读这篇文章，你可以在[这里](/hillelwayne)订阅。每周更新一次。我的主网站在[这里](https://www.hillelwayne.com)。

My new book, Logic for Programmers, is now in early access! Get it [here](https://leanpub.com/logic/).

我的新书《程序员逻辑学》现已开放抢先体验！可以在[这里](https://leanpub.com/logic/)获取。

---

## 批判性思考评论

这篇文章虽然简短，但透露了几个值得思考的技术写作和软件工程问题：

**1. 关于"谷壳"（Chaff）的价值**
作者在写书过程中产生了大量未使用的内容，这实际上是知识创作的常态。很多时候，被舍弃的"谷壳"并非没有价值，而是不适合特定的表达形式。对于技术写作者来说，如何管理这些副产品是一个值得思考的问题。也许可以建立个人知识库，将这些内容以不同的形式（如博客、小册子、代码示例）发布。

**2. Z3 和 SMT 求解器的学习曲线**
从作者提到的困难可以看出，即使是经验丰富的程序员，在使用形式化工具时也会遇到挑战。特别是关于全函数（total functions）、量词处理、以及求解器的不可判定性等问题，这些都是形式化方法中的核心概念，但对初学者来说门槛很高。这提醒我们，在推广形式化验证工具时，需要更好的教育材料和更友好的抽象层。

**3. 营销与内容质量的平衡**
作者提到希望营销材料"不乏味"，这是一个很好的态度。太多技术书籍的营销内容只是枯燥的功能列表，而作者选择通过分享有趣的技术内容来营销，这种方式更尊重读者的智力，也更能建立长期的信任关系。

**4. 求解器的黑箱问题**
作者提到数组示例返回了意外的结果（2 而不是 99999999），这揭示了 SMT 求解器作为复杂黑箱系统的特性。即使是专家也难以预测其行为，这对依赖这些工具进行关键验证的场景提出了挑战——当求解器给出意外结果时，我们如何确定是自己建模错了，还是求解器内部有特殊的优化逻辑？
