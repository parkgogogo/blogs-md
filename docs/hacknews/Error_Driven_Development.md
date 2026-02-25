# Error-Driven Development
# 错误驱动开发

It is often said that the compilation time of compiled languages slows down development. It makes sense - any time you make a change and want to see the results, you have to wait for your code to compile. If you were using an interpreted language, you could run it and see the results right away.

人们常说编译型语言的编译时间会拖慢开发速度。这说得通——每次你做出修改并想查看结果时，都必须等待代码编译。如果你使用的是解释型语言，就可以直接运行并立即看到结果。

But this assumes that your code is correct. Compilers often operate in two phases - a typechecking phase, and a codegen phase. Usually it is the codegen phase that is slow - type checking is very fast.

但这假设你的代码是正确的。编译器通常分两个阶段运行——类型检查阶段和代码生成阶段。通常代码生成阶段才是慢的——类型检查非常快。

(It's sometimes said that the reason rust compilation times are slow is because rust does so much static analysis, but the vast majority of the compilation time is actually from codegen.)

（有时人们说 Rust 编译时间慢是因为 Rust 做了大量的静态分析，但实际上编译时间的绝大部分都花在代码生成上。）

And if your code is incorrect in a way that can be detected by the type checker, you can often get a much faster development cycle in a compiled language, because instead of needing to run your code and actually exercise the error (slow), the typechecker can detect it and tell you exactly where the mistake is (fast).

如果你的代码以类型检查器能够检测到的方式出错，你通常可以在编译型语言中获得快得多的开发周期，因为不需要运行代码并实际触发错误（慢），类型检查器就能检测到它并准确告诉你错误在哪里（快）。

If you have good IDE integration in your language, you often get those red squiggly underlines around areas that need fixing. What feedback loop could be faster than that? You don't even have to go into your terminal, you can see the errors immediately.

如果你的语言有良好的 IDE 集成，你经常会在需要修复的地方看到红色波浪线。还有什么反馈循环能比这个更快？你甚至不需要打开终端，就能立即看到错误。

This leads to a different mindset towards editing code. It takes some getting used to, but after a while of using a compiled语言, you can predict what errors you'll get from a certain change, and then use those errors to navigate around the code.

这导致了一种不同的代码编辑心态。这需要一些时间来适应，但在使用编译型语言一段时间后，你可以预测某个更改会产生什么错误，然后利用这些错误来导航代码。

For example, in Rust, the compiler checks that all `match` statements on enums handle every case. That means that after adding a new variant to an enum, the compiler will notify you of all the `match` statements that need a new case.

例如，在 Rust 中，编译器会检查枚举上的所有 `match` 语句是否处理了每一种情况。这意味着在向枚举添加新变体后，编译器会通知你所有需要新分支的 `match` 语句。

That makes adding a new variant to an enum extremely easy. In general, if you know that all of the errors that would result from a change you want to make would be detected by the type checker, it is usually extremely easy to make that change.

这使得向枚举添加新变体变得极其容易。一般来说，如果你知道你想做的更改所产生的所有错误都会被类型检查器检测到，那么做那个改变通常就非常容易。

## Compounding
## 复利效应

This has massive ramifications for your code. Since these changes are easy, you can do them as soon as you feel like it makes your code better. Often these changes improve the architecture of your codebase. Since you do these changes more quickly and more often, you have more cycles of architectural-improvement in the same amount of time.

这对你的代码有巨大的影响。因为这些改变很容易，你可以在你觉得能让代码更好的时候立即去做。这些改变通常会改善代码库的架构。因为你做得更快更频繁，在相同时间内你就有更多的架构改进周期。

## Documentation
## 文档

Another way of looking at types is that they're documentation. For example, imagine a function takes a `NonZeroU64`. That is clearly documentation that the function must not be passed `0` for that argument. While types don't remove the need for explicit documentation, they do provide some documentation that the language forces you to添加, can't be ignored, and is always up-to-date.

看待类型的另一种方式是它们就是文档。例如，想象一个函数接受 `NonZeroU64`。这显然是在说明该函数不能为那个参数传入 `0`。虽然类型不能消除显式文档的需要，但它们确实提供了一些语言强制你添加的、不能被忽视的、始终最新的文档。

Suppose you upgrade a version of dependency. A function in the old version of a dependency took a `u64`, while the function in the new version of the dependency takes a `NonZeroU64`. You don't have to read a migration guide or look at a changelog to detect this, and you don't have to poke around your app waiting for a crash. You will get an error the first time you compile, and the error will explain that you passed a `u64` but should have passed a `NonZeroU64`. This makes upgrading dependencies much easier, which makes it easier to keep your dependencies up to date.

假设你升级了一个依赖的版本。旧版本依赖中的一个函数接受 `u64`，而新版本的依赖中的函数接受 `NonZeroU64`。你不需要阅读迁移指南或查看更新日志来发现这一点，也不需要在应用中四处试探等待崩溃。你在第一次编译时就会得到一个错误，错误会解释说你传了 `u64` 但应该传 `NonZeroU64`。这使得升级依赖变得容易得多，进而让你更容易保持依赖的更新。

(Of course, the best dependency upgrade is the one that introduces no breaking changes at all. But often breaking changes are introduced by accident. Again, types help us here. [`cargo-semver-checks`](https://crates.io/crates/cargo-semver-checks) looks at the type签名 of the old version and the new version of your library, and scans the changes for common sources of breakage. Does anything like this exist for Python? I'm not sure, but I bet it would be much harder to implement.)

（当然，最好的依赖升级是根本不引入破坏性变更的那种。但破坏性变更往往是意外引入的。再次说明，类型在这里帮助我们。[`cargo-semver-checks`](https://crates.io/crates/cargo-semver-checks) 会查看库旧版本和新版本的类型签名，扫描变更中常见的破坏来源。Python 有类似的东西吗？我不确定，但我打赌它会难实现得多。）

---

## Critical Thinking Commentary / 批判性思考

本文提出的"错误驱动开发"（Error-Driven Development, EDD）概念颇具启发性，但我们需要以批判性思维来审视其适用范围和潜在局限：

### 1. 前提假设的局限

作者假设"代码不正确"是常态，但对于原型开发、探索性编程或数据科学领域，代码的快速迭代和试验往往比类型安全更重要。在这些场景下，解释型语言（如 Python、JavaScript）的灵活性可能比编译器的严格检查更有价值。

### 2. 学习曲线的忽视

Rust 等强类型语言确实有强大的类型系统，但其学习曲线陡峭。对于团队项目，引入强类型语言可能增加开发人员的培训成本，短期内反而降低开发效率。EDD 的收益是长期的，但成本是即时的。

### 3. 类型系统的双刃剑

虽然类型可以作为"强制文档"，但过度复杂的类型系统（如 Haskell 的高级类型特性）可能导致代码难以阅读，反而增加了认知负担。`NonZeroU64` 这样的例子很好，但现实中我们更常遇到晦涩难懂的类型签名。

### 4. 对动态语言生态的低估

作者质疑 Python 是否有类似 `cargo-semver-checks` 的工具。实际上，Python 的类型提示（type hints）和 `mypy` 等工具正在快速发展，结合 IDE 支持（如 Pylance），也能提供类似的静态检查能力。动态语言正在"偷师"静态语言的优点。

### 5. 编译时间仍是瓶颈

虽然作者区分了类型检查和代码生成，但在大型 Rust 项目中，即使只是类型检查，等待时间也可能显著影响开发体验。EDD 的"快速反馈"假设在大型代码库中可能不成立。

### 结论

EDD 是一个有价值的视角，提醒我们错误信息本身可以成为开发工具。但它并非银弹——最佳实践可能是"混合方法"：在核心架构使用强类型语言获得 EDD 收益，在探索性代码或胶水代码中使用动态语言保持灵活性。
