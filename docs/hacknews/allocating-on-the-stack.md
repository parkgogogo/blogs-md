---
title: "Allocating on the Stack"
url: "https://go.dev/blog/allocation-optimizations"
rating: 9
category: "systems-programming"
date: "2026-02-28"
---

# Allocating on the Stack

We're always looking for ways to make Go programs faster. In the last 2 releases, we have concentrated on mitigating a particular source of slowness, heap allocations. Each time a Go program allocates memory from the heap, there's a fairly large chunk of code that needs to run to satisfy that allocation. In addition, heap allocations present additional load on the garbage collector. Even with recent enhancements like [Green Tea](/blog/greenteagc), the garbage collector still incurs substantial overhead.

So we've been working on ways to do more allocations on the stack instead of the heap. Stack allocations are considerably cheaper to perform (sometimes completely free). Moreover, they present no load to the garbage collector, as stack allocations can be collected automatically together with the stack frame itself. Stack allocations also enable prompt reuse, which is very cache friendly.

## Stack allocation of constant-sized slices

Consider the task of building a slice of tasks to process:

```go
func process(c chan task) {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

Let's walk through what happens at runtime when pulling tasks from the channel `c` and adding them to the slice `tasks`.

On the first loop iteration, there is no backing store for `tasks`, so `append` has to allocate one. Because it doesn't know how big the slice will eventually be, it can't be too aggressive. Currently, it allocates a backing store of size 1.

On the second loop iteration, the backing store now exists, but it is full. `append` again has to allocate a new backing store, this time of size 2. The old backing store of size 1 is now garbage.

On the third loop iteration, the backing store of size 2 is full. `append` *again* has to allocate a new backing store, this time of size 4. The old backing store of size 2 is now garbage.

On the fourth loop iteration, the backing store of size 4 has only 3 items in it. `append` can just place the item in the existing backing store and bump up the slice length. Yay! No call to the allocator for this iteration.

On the fifth loop iteration, the backing store of size 4 is full, and `append` again has to allocate a new backing store, this time of size 8.

And so on. We generally double the size of the allocation each time it fills up, so we can eventually append most new tasks to the slice without allocation. But there is a fair amount of overhead in the "startup" phase when the slice is small. During this startup phase we spend a lot of time in the allocator, and produce a bunch of garbage, which seems pretty wasteful. And it may be that in your program, the slice never really gets large. This startup phase may be all you ever encounter.

If this code was a really hot part of your program, you might be tempted to start the slice out at a larger size, to avoid all of these allocations.

```go
func process2(c chan task) {
    tasks := make([]task, 0, 10) // probably at most 10 tasks
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

This is a reasonable optimization to do. It is never incorrect; your program still runs correctly. If the guess is too small, you get allocations from append as before. If the guess is too large, you waste some memory.

If your guess for the number of tasks was a good one, then there's only one allocation site in this program. The `make` call allocates a slice backing store of the correct size, and `append` never has to do any reallocation.

The surprising thing is that if you benchmark this code with 10 elements in the channel, you'll see that you didn't reduce the number of allocations to 1, you reduced the number of allocations to **0**!

The reason is that the compiler decided to allocate the backing store on the stack. Because it knows what size it needs to be (10 times the size of a task) it can allocate storage for it in the stack frame of `process2` instead of on the heap[^1]. Note that this depends on the fact that the backing store does not escape to the heap inside of `processAll`.

## Stack allocation of variable-sized slices

But of course, hard coding a size guess is a bit rigid. Maybe we can pass in an estimated length?

```go
func process3(c chan task, lengthGuess int) {
    tasks := make([]task, 0, lengthGuess)
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

This lets the caller pick a good size for the `tasks` slice, which may vary depending on where this code is being called from.

Unfortunately, in Go 1.24 the non-constant size of the backing store means the compiler can no longer allocate the backing store on the stack. It will end up on the heap, converting our 0-allocation code to 1-allocation code. Still better than having append do all the intermediate allocations, but unfortunate.

But never fear, Go 1.25 is here!

Imagine you decide to do the following, to get the stack allocation only in cases where the guess is small:

```go
func process4(c chan task, lengthGuess int) {
    var tasks []task
    if lengthGuess <= 10 {
        tasks = make([]task, 0, 10)
    } else {
        tasks = make([]task, 0, lengthGuess)
    }
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

Kind of ugly, but it would work. When the guess is small, you use a constant size `make` and thus a stack-allocated backing store, and when the guess is larger you use a variable size `make` and allocate the backing store from the heap.

But in Go 1.25, you don't need to head down this ugly road. The Go 1.25 compiler does this transformation for you! For certain slice allocation locations, the compiler automatically allocates a small (currently 32-byte) slice backing store, and uses that backing store for the result of the `make` if the size requested is small enough. Otherwise, it uses a heap allocation as normal.

In Go 1.25, `process3` performs zero heap allocations, if `lengthGuess` is small enough that a slice of that length fits into 32 bytes. (And of course that `lengthGuess` is a correct guess for how many items are in `c`.)

We're always improving the performance of Go, so upgrade to the latest Go release and be [surprised by](https://go.dev/dl/) how much faster and memory efficient your program becomes!

## Stack allocation of append-allocated slices

Ok, but you still don't want to have to change your API to add this weird length guess. Anything else you could do?

Upgrade to Go 1.26!

```go
func process(c chan task) {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

In Go 1.26, we allocate the same kind of small, speculative backing store on the stack, but now we can use it directly at the append site.

On the first loop iteration, there is no backing store for `tasks`, so `append` uses a small, stack-allocated backing store as the first allocation. If, for instance, we can fit 4 tasks in that backing store, the first `append` allocates a backing store of length 4 from the stack. The next 3 loop iterations append directly to the stack backing store, requiring no allocation.

On the 4th iteration, the stack backing store is finally full and we have to go to the heap for more backing store. But we have avoided almost all of the startup overhead described earlier in this article. No heap allocations of size, 1, 2, and 4, and none of the garbage that they eventually become. If your slices are small, maybe you will never have a heap allocation.

## Stack allocation of append-allocated escaping slices

Ok, this is all good when the `tasks` slice doesn't escape. But what if I'm returning the slice? Then it can't be allocated on the stack, right?

Right! The backing store for the slice returned by `extract` below can't be allocated on the stack, because the stack frame for `extract` disappears when `extract` returns.

```go
func extract(c chan task) []task {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    return tasks
}
```

But you might think, the returned slice can't be allocated on the stack. But what about all those intermediate slices that just become garbage? Maybe we can allocate those on the stack?

```go
func extract2(c chan task) []task {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    tasks2 := make([]task, len(tasks))
    copy(tasks2, tasks)
    return tasks2
}
```

Then the `tasks` slice never escapes `extract2`. It can benefit from all of the optimizations described above. Then at the very end of `extract2`, when we know the final size of the slice, we do one heap allocation of the required size, copy our tasks into it, and return the copy.

But do you really want to write all that additional code? It seems error prone. Maybe the compiler can do this transformation for us?

In Go 1.26, it can!

For escaping slices, the compiler will transform the original `extract` code to something like this:

```go
func extract3(c chan task) []task {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    tasks = runtime.move2heap(tasks)
    return tasks
}
```

`runtime.move2heap` is a special compiler+runtime function that is the identity function for slices that are already allocated in the heap. For slices that are on the stack, it allocates a new slice on the heap, copies the stack-allocated slice to the heap copy, and returns the heap copy.

This ensures that for our original `extract` code, if the number of items fits in our small stack-allocated buffer, we perform exactly 1 allocation of exactly the right size. If the number of items exceeds the capacity our small stack-allocated buffer, we do our normal doubling-allocation once the stack-allocated buffer overflows.

The optimization that Go 1.26 does is actually better than the hand-optimized code, because it does not require the extra allocation+copy that the hand-optimized code always does at the end. It requires the allocation+copy only in the case that we've exclusively operated on a stack-backed slice up to the return point.

We do pay the cost for a copy, but that cost is almost completely offset by the copies in the startup phase that we no longer have to do. (In fact, the new scheme at worst has to copy one more element than the old scheme.)

## Wrapping up

Hand optimization can still be beneficial, especially if you have a good estimate of the slice size ahead of time. But hopefully the compiler will now catch a lot of the simple cases for you and allow you to focus on the remaining ones that really matter.

There are a lot of details that the compiler needs to ensure to get all these optimizations right. If you think that one of these optimizations is causing correctness or (negative) performance issues for you, you can turn them off with `-gcflags=all=-d=variablemakehash=n`. If turning these optimizations off helps, please file an issue so we can investigate.

## Footnotes

[^1]: Go stacks do not have any alloca-style mechanism for dynamically-sized stack frames. All Go stack frames are constant sized.

---

# 中文翻译

# 栈上分配内存

我们一直在寻找让 Go 程序更快的方法。在最近两个版本中，我们专注于缓解一个特定的性能瓶颈：堆内存分配。每次 Go 程序从堆中分配内存时，都需要运行相当多的代码来满足该分配请求。此外，堆分配会给垃圾回收器带来额外的负担。即使有了最近的 [Green Tea](/blog/greenteagc) 等优化改进，垃圾回收器仍然会产生相当大的开销。

因此，我们一直在研究如何在栈上而不是堆上进行更多的内存分配。栈分配的执行成本要低得多（有时甚至完全免费）。而且，它们不会给垃圾回收器带来任何负担，因为栈分配可以与栈帧本身一起自动回收。栈分配还能实现快速的内存复用，这对 CPU 缓存非常友好。

## 常量大小切片的栈分配

考虑这样一个任务：构建一个待处理任务的切片：

```go
func process(c chan task) {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

让我们逐步分析运行时从通道 `c` 拉取任务并添加到切片 `tasks` 时会发生什么。

在第一次循环迭代时，`tasks` 还没有底层存储空间，所以 `append` 必须分配一个。因为它不知道切片最终会有多大，所以不能过于激进。目前，它会分配大小为 1 的底层存储空间。

在第二次循环迭代时，底层存储空间已经存在，但它已满。`append` 再次需要分配一个新的底层存储空间，这次大小为 2。旧的、大小为 1 的底层存储空间现在变成了垃圾。

在第三次循环迭代时，大小为 2 的底层存储空间已满。`append` **再次**需要分配一个新的底层存储空间，这次大小为 4。旧的、大小为 2 的底层存储空间现在变成了垃圾。

在第四次循环迭代时，大小为 4 的底层存储空间里只有 3 个元素。`append` 可以直接将元素放入现有的底层存储空间，并增加切片长度。太好了！这次迭代不需要调用分配器。

在第五次循环迭代时，大小为 4 的底层存储空间已满，`append` 再次需要分配一个新的底层存储空间，这次大小为 8。

依此类推。我们通常每次填满时将分配大小翻倍，这样最终可以将大多数新任务追加到切片中而无需额外分配。但在切片较小时的"启动"阶段，会有相当多的开销。在这个启动阶段，我们在分配器中花费了大量时间，并产生了大量垃圾，这似乎相当浪费。而且在你的程序中，切片可能永远不会变得很大。这个启动阶段可能是你唯一会遇到的阶段。

如果这段代码是你程序中非常热的执行路径，你可能会忍不住让切片从更大的大小开始，以避免所有这些分配。

```go
func process2(c chan task) {
    tasks := make([]task, 0, 10) // 可能最多 10 个任务
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

这是一个合理的优化。它永远不会是错误的；你的程序仍然正确运行。如果猜测的大小太小，你会像以前一样从 append 获得分配。如果猜测的大小太大，你会浪费一些内存。

如果你对任务数量的猜测是准确的，那么这个程序中只有一个分配点。`make` 调用分配了一个大小正确的切片底层存储空间，`append` 永远不需要进行任何重新分配。

令人惊讶的是，如果你用通道中的 10 个元素对这段代码进行基准测试，你会发现你没有将分配次数减少到 1 次，而是减少到了 **0** 次！

原因是编译器决定在栈上分配底层存储空间。因为它知道需要的大小（10 倍的任务大小），所以它可以在 `process2` 的栈帧中而不是在堆上为其分配存储空间[^1]。请注意，这取决于底层存储空间在 `processAll` 内部不会逃逸到堆的事实。

## 变量大小切片的栈分配

但是当然，硬编码一个大小猜测有点僵化。也许我们可以传入一个估计的长度？

```go
func process3(c chan task, lengthGuess int) {
    tasks := make([]task, 0, lengthGuess)
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

这让调用者可以为 `tasks` 切片选择一个合适的大小，这可能因调用此代码的位置而异。

不幸的是，在 Go 1.24 中，底层存储空间的非常量大小意味着编译器不能再在栈上分配底层存储空间。它将最终在堆上，将我们零分配的代码转换为一次分配的代码。仍然比让 append 做所有中间分配要好，但很遗憾。

但是别担心，Go 1.25 来了！

想象一下，你决定这样做，只在猜测值较小时获得栈分配：

```go
func process4(c chan task, lengthGuess int) {
    var tasks []task
    if lengthGuess <= 10 {
        tasks = make([]task, 0, 10)
    } else {
        tasks = make([]task, 0, lengthGuess)
    }
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

有点丑陋，但它是有效的。当猜测值较小时，你使用常量大小的 `make`，从而获得栈分配的底层存储空间；当猜测值较大时，你使用变量大小的 `make`，从堆中分配底层存储空间。

但在 Go 1.25 中，你不需要走这条丑陋的路。Go 1.25 编译器会自动为你做这个转换！对于某些切片分配位置，编译器会自动分配一个小的（目前为 32 字节）切片底层存储空间，如果请求的大小足够小，就将该底层存储空间用于 `make` 的结果。否则，它会像平常一样使用堆分配。

在 Go 1.25 中，如果 `lengthGuess` 足够小，使得该长度的切片能放入 32 字节，`process3` 就执行零次堆分配。（当然，前提是 `lengthGuess` 正确猜测了 `c` 中的项目数量。）

我们一直在改进 Go 的性能，所以请升级到最新的 Go 版本，[惊喜地发现](https://go.dev/dl/)你的程序变得更快、更省内存了！

## append 分配切片的栈分配

好的，但你还是不想为了添加这个奇怪的长度猜测而改变你的 API。还有其他办法吗？

升级到 Go 1.26！

```go
func process(c chan task) {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    processAll(tasks)
}
```

在 Go 1.26 中，我们在栈上分配同样的小型、推测性底层存储空间，但现在我们可以直接在 append 位置使用它。

在第一次循环迭代时，`tasks` 还没有底层存储空间，所以 `append` 使用栈分配的小型底层存储空间作为第一次分配。例如，如果我们在该底层存储空间中能容纳 4 个任务，第一次 `append` 就从栈分配一个长度为 4 的底层存储空间。接下来的 3 次循环迭代直接追加到栈底层存储空间，不需要分配。

在第 4 次迭代时，栈底层存储空间终于满了，我们必须去堆中获取更多底层存储空间。但我们已经避免了本文前面描述的大部分启动开销。没有大小为 1、2 和 4 的堆分配，也没有它们最终变成的垃圾。如果你的切片很小，也许你永远不会进行堆分配。

## 逃逸切片的 append 分配栈分配

好的，当 `tasks` 切片不逃逸时这一切都很好。但如果我要返回切片呢？那它就不能在栈上分配了，对吧？

对的！下面 `extract` 返回的切片的底层存储空间不能在栈上分配，因为当 `extract` 返回时，`extract` 的栈帧就消失了。

```go
func extract(c chan task) []task {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    return tasks
}
```

但你可能会想，返回的切片不能在栈上分配。但那些变成垃圾的中间切片呢？也许我们可以在栈上分配那些？

```go
func extract2(c chan task) []task {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    tasks2 := make([]task, len(tasks))
    copy(tasks2, tasks)
    return tasks2
}
```

然后 `tasks` 切片永远不会逃逸出 `extract2`。它可以从上述所有优化中受益。然后在 `extract2` 的最后，当我们知道切片的最终大小时，我们进行一次所需大小的堆分配，将任务复制到其中，并返回副本。

但你真的想写所有这些额外的代码吗？它似乎容易出错。也许编译器可以为我们做这个转换？

在 Go 1.26 中，它可以！

对于逃逸切片，编译器会将原始的 `extract` 代码转换为类似这样的代码：

```go
func extract3(c chan task) []task {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t)
    }
    tasks = runtime.move2heap(tasks)
    return tasks
}
```

`runtime.move2heap` 是一个特殊的编译器+运行时函数，对于已经在堆中分配的切片，它相当于恒等函数。对于在栈上的切片，它会在堆上分配一个新切片，将栈分配的切片复制到堆副本中，并返回堆副本。

这确保了对于原始的 `extract` 代码，如果项目数量适合我们小型栈分配缓冲区，我们就只执行一次大小完全正确的分配。如果项目数量超过了我们小型栈分配缓冲区的容量，一旦栈分配缓冲区溢出，我们就执行正常的双倍分配。

Go 1.26 做的优化实际上比手工优化的代码更好，因为它不需要手工优化代码在末尾总是执行的额外分配+复制。它只在我们在返回点之前完全在栈支持的切片上操作的情况下才需要分配+复制。

我们确实要支付复制的成本，但这个成本几乎完全被我们在启动阶段不再需要做的复制所抵消。（事实上，在最坏情况下，新方案比旧方案多复制一个元素。）

## 总结

手工优化仍然可能是有益的，特别是如果你能提前很好地估计切片大小。但希望编译器现在能为你捕获很多简单的情况，让你可以专注于真正重要的剩余情况。

编译器需要确保很多细节才能正确实现所有这些优化。如果你认为这些优化中的某一个正在导致正确性或（负面）性能问题，你可以用 `-gcflags=all=-d=variablemakehash=n` 关闭它们。如果关闭这些优化有帮助，请提交一个 issue 以便我们调查。

## 脚注

[^1]: Go 栈没有任何 alloca 风格的动态大小栈帧机制。所有 Go 栈帧都是固定大小的。
