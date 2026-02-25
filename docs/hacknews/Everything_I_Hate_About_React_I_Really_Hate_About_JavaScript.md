# Everything I Hate About React, I Really Hate About JavaScript

# 我讨厌 React 的一切，实际上都是讨厌 JavaScript

The main thing people hate about React is not React's fault at all, but is actually caused by a design flaw in JavaScript. (Or TypeScript, it makes no difference for the purposes of this post.) Let me show you what I mean.

人们讨厌 React 的主要原因根本不是 React 的错，实际上是 JavaScript 的一个设计缺陷造成的。（或者 TypeScript，对于本文的目的来说没有区别。）让我来说明我的意思。

---

## The Simple Component That Isn't
## 看似简单的组件

So you're writing a simple storefront:

假设你正在编写一个简单的商店页面：

```jsx
function Store() {
  const [cart, setCart] = useState([]);
  
  return (
    <>
      <ProductListings setCart={setCart} />
      <Button onClick={() => checkout(cart)}>
        Checkout
      </Button>
    </>
  );
}
```

Looks fine, right? Wrong! This component has a subtle but annoying problem.

看起来没问题，对吧？错了！这个组件有一个微妙但令人讨厌的问题。

Look at that anonymous function we're passing to `Button`: `() => checkout(cart)`. This creates a brand new function every single render. Which means if `Button` is a memoized component (let's say it's expensive to render for some reason), it doesn't matter, it's going to re-render every single time anyway because React sees a "different" function being passed as a prop.

看看我们传递给 `Button` 的那个匿名函数：`() => checkout(cart)`。这在每次渲染时都会创建一个全新的函数。这意味着如果 `Button` 是一个被记忆化的组件（假设由于某种原因渲染成本很高），那也没用，它每次都会重新渲染，因为 React 看到的是一个作为 prop 传递的"不同"函数。

---

## The "Solution" That Isn't
## 并非真正的"解决方案"

OK, so React gives us `useCallback` to fix this:

好吧，React 给了我们 `useCallback` 来解决这个问题：

```jsx
function ShoppingCart() {
  const [items, setItems] = useState([]);
  
  const handleCheckout = useCallback(() => {
    checkout(items);
  }, [items]);
  
  return (
    <>
      <Store onAddItem={setItems} />
      <Button onClick={handleCheckout}>
        Checkout
      </Button>
    </>
  );
}
```

Great, problem solved! Except... wait. Now let's say we want to transform our items before checkout. Maybe normalize them to lowercase or something:

太好了，问题解决了！但是……等等。现在假设我们想在结账前转换商品数据。也许将它们规范化为小写之类的：

```jsx
function ShoppingCart() {
  const [items, setItems] = useState([]);
  
  const normalizedItems = items.map(item => item.toLowerCase());
  
  const handleCheckout = useCallback(() => {
    checkout(normalizedItems);
  }, [normalizedItems]);
  
  return (
    <>
      <Store onAddItem={setItems} />
      <Button onClick={handleCheckout}>
        Checkout
      </Button>
    </>
  );
}
```

Now we're back to square one. That `items.map()` creates a new array every render, which means `normalizedItems` has a different reference every time, which means `useCallback` generates a new function every time, completely defeating its purpose.

现在我们回到了原点。那个 `items.map()` 每次渲染都会创建一个新数组，这意味着 `normalizedItems` 每次都有不同的引用，这意味着 `useCallback` 每次都会生成一个新函数，完全违背了它的初衷。

---

## The Cascade of Memoization
## 记忆化的级联效应

So now we need `useMemo`:

所以现在我们需要 `useMemo`：

```jsx
function ShoppingCart() {
  const [items, setItems] = useState([]);
  
  const normalizedItems = useMemo(
    () => items.map(item => item.toLowerCase()),
    [items]
  );
  
  const handleCheckout = useCallback(() => {
    checkout(normalizedItems);
  }, [normalizedItems]);
  
  return (
    <>
      <Store onAddItem={setItems} />
      <Button onClick={handleCheckout}>
        Checkout
      </Button>
    </>
  );
}
```

This is what I call the memoization cascade. You add one `useCallback`, which requires you to add a `useMemo`, which might require another `useMemo` somewhere else. Now our component is literally more memoization boilerplate than actual logic.

这就是我所说的记忆化级联。你添加一个 `useCallback`，就需要添加一个 `useMemo`，这可能又需要在其他地方添加另一个 `useMemo`。现在我们的组件实际上记忆化样板代码比真正的业务逻辑还多。

---

## The Real Problem: JavaScript's Equality
## 真正的问题：JavaScript 的相等性

Here's the thing that really gets me: **none of this would be a problem if JavaScript just had structural equality instead of reference equality**.

真正让我抓狂的是：**如果 JavaScript 有结构相等性而不是引用相等性，这些问题都不会存在**。

In JavaScript, `[1, 2, 3] === [1, 2, 3]` is `false`. Two arrays with the exact same contents are considered different because they're different objects in memory.

在 JavaScript 中，`[1, 2, 3] === [1, 2, 3]` 的结果是 `false`。两个内容完全相同的数组被认为是不同的，因为它们在内存中是不同的对象。

The thing I hate the most about this design decision is that it's literally never what I want. Literally not once in my entire life have I said "I want to tell if these two arrays are referentially equal." I always just want to know if they have the same items.

我最讨厌这个设计决定的一点是，它从来都不是我想要的。在我的一生中，我从未说过"我想判断这两个数组是否是引用相等的"。我总是只想知道它们是否有相同的元素。

What's the workaround people use in practice? This monstrosity:

人们在实践中使用的变通方法是什么？这个可怕的写法：

```js
JSON.stringify(array1) === JSON.stringify(array2)
```

We're serializing data structures to strings to compare them. Think about how absurd that is for a second. The *one* benefit of reference equality was that it was faster than structural equality, because it's just one pointer比较. So ostensibly in the name of performance, we've ended up in a situation where the only way to check if two objects are equal involves string allocations.

我们将数据结构序列化为字符串来进行比较。稍微想一下这是多么荒谬。引用相等性的*唯一*好处是它比结构相等性更快，因为它只是一个指针比较。所以表面上以性能的名义，我们最终陷入了一种情况：检查两个对象是否相等的唯一方法涉及字符串分配。

Don't get me wrong. Before React, web development was a horrible mess of having to keep track of what parts of the DOM to update on every state change. (And forgetting to update something was a very common source of bugs.) React completely solved that, replaced it with the opposite problem: it's now extremely annoying to help React figure out what _not_ to update.

别误会我的意思。在 React 之前，Web 开发是一团糟，必须跟踪每次状态变化时要更新 DOM 的哪些部分。（忘记更新某些东西是非常常见的 bug 来源。）React 完全解决了这个问题，但取而代之的是一个相反的问题：现在帮助 React 确定*不要*更新什么变得非常烦人。

Even if this doesn't causes noticeable performance issues in your app, it's philosophically annoying. The computer is wasting work recomputing things that haven't changed, and the only reason is what feels like a language级别的 bug. You add one innocent `.map()` and suddenly your whole component tree is re-rendering for no reason. Fortunately for my argument, this are not just performance issues.

即使这不会在你的应用中造成明显的性能问题，从哲学上讲也很烦人。计算机正在浪费资源重新计算那些没有改变的东西，而唯一的原因感觉就像是一个语言级别的 bug。你添加一个无辜的 `.map()`，突然你的整个组件树无缘无故地重新渲染了。幸运的是，对于我的论点来说，这些不仅仅是性能问题。

---

## This is a correctness issue
## 这是一个正确性问题

Consider this component, intended to notify your server when the user's shopping cart changes:

考虑这个组件，旨在当用户的购物车变化时通知服务器：

```jsx
function ShoppingCart() {
  const [items, setItems] = useState([]);

  const normalizedItems = items.map(item => item.toLowerCase());
  
  useEffect(() => {
    notifyServer(normalizedItems);
  }, [normalizedItems]); // oops! this effect will run every render
  
  // ...
}
```

[This exact issue was responsible for a recent CloudFlare outage](https://blog.cloudflare.com/deep-dive-into-cloudflares-sept-12-dashboard-and-api-outage/)

[这个确切的问题导致了最近 CloudFlare 的一次宕机](https://blog.cloudflare.com/deep-dive-into-cloudflares-sept-12-dashboard-and-api-outage/)

> The incident's impact stemmed from several issues, but the immediate trigger was a bug in the dashboard. This bug caused repeated, unnecessary calls to the Tenant Service API. The API calls were managed by a React useEffect hook, but we mistakenly included a problematic object in its dependency array. Because this object was recreated on every state or prop change, React treated it as "always new," causing the useEffect to re-run each time. As a result, the API call executed many times during a single dashboard render instead of just once. This behavior coincided with a service update to the Tenant Service API, compounding instability and ultimately overwhelming the service, which then failed to recover.
> 
> 事件的影响源于几个问题，但直接的触发因素是仪表板中的一个 bug。这个 bug 导致了对 Tenant Service API 的重复、不必要的调用。API 调用由 React useEffect hook 管理，但我们错误地在依赖数组中包含了一个有问题的对象。因为这个对象在每次状态或 prop 变化时都被重新创建，React 将其视为"总是新的"，导致 useEffect 每次都会重新运行。结果，API 调用在单次仪表板渲染期间执行了多次，而不是仅执行一次。这种行为与 Tenant Service API 的服务更新同时发生，加剧了不稳定性，最终导致服务不堪重负而无法恢复。

> When the Tenant Service became overloaded, it had an impact on other APIs and the dashboard because Tenant Service is part of our API request authorization logic.  Without Tenant Service, API request authorization can not be evaluated.  When authorization evaluation fails, API requests return 5xx status codes.
> 
> 当 Tenant Service 过载时，它对其他 API 和仪表板产生了影响，因为 Tenant Service 是我们 API 请求授权逻辑的一部分。没有 Tenant Service，就无法评估 API 请求授权。当授权评估失败时，API 请求返回 5xx 状态码。

---

## Enter the React Compiler
## React 编译器登场

The React team apparently agrees this is a problem, because they invented the React Compiler. This is just a pass over your code that automatically inserts `useMemo` and `useCallback` everywhere for you.

React 团队显然同意这是一个问题，因为他们发明了 React 编译器。这只是对你的代码进行一次遍历，自动为你到处插入 `useMemo` 和 `useCallback`。

I don't know, this feels like an extremely complicated and unsatisfying solution to the problem of equality not doing what it should. But I thought I'd give it a try anyway. Of course, I immediately discovered the React compiler is not an actual solution to this problem.

我不知道，这感觉像是一个极其复杂且不能令人满意的解决方案，用来解决相等性不按预期工作的问题。但我想我还是试试看。当然，我立即发现 React 编译器并不是这个问题的真正解决方案。

---

## The Compiler's Weird Limitations
## 编译器的奇怪限制

The React Compiler doesn't necessarily optimize every component. If your component already uses `useMemo` or `useCallback`, in some cases it will decide not to optimize that component.

React 编译器不一定优化每个组件。如果你的组件已经使用了 `useMemo` 或 `useCallback`，在某些情况下它会决定不优化该组件。

So consider the case where you have an extensive computation in a component, and you want to add a useMemo, and you discover that this is a useMemo that the React compiler does not agree with.

所以考虑一下这种情况：你在一个组件中有大量的计算，你想添加一个 useMemo，然后你发现这是一个 React 编译器不同意的 useMemo。

Now you have a [choice](https://github.com/facebook/react/issues/34289):

现在你有两个[选择](https://github.com/facebook/react/issues/34289)：

- Remove your legitimate `useMemo` (maybe you're memoizing something genuinely expensive) to let the compiler work
- Keep your `useMemo` and remember that this component is now in a separate magisterium, outside the grace of the React Compiler, and you need to manually add all the other memoization yourself

- 移除你合法的 `useMemo`（也许你正在记忆化某个真正昂贵的计算）来让编译器工作
- 保留你的 `useMemo` 并记住这个组件现在处于一个单独的管辖区域，在 React 编译器的恩典之外，你需要手动添加所有其他的记忆化

Neither is great. Because the compiler doesn't work on all components, you're left in a weird headspace. Either you:

两个选择都不好。因为编译器不能在所有组件上工作，你陷入了一种奇怪的思维状态。要么你：

- Keep track of which components it optimizes (good luck with that)
- Or code as if it doesn't exist and treat it as an occasional performance bonus

- 跟踪它优化了哪些组件（祝你好运）
- 或者像它不存在一样编码，把它当作偶尔的性能够红利

The second option seems like the only practical approach, which means the compiler doesn't actually save you any effort. You still need to think about when you need memoization for correctness.

第二个选择似乎是唯一实用的方法，这意味着编译器实际上并没有为你节省任何精力。你仍然需要考虑什么时候需要记忆化来保证正确性。

---

## The Root Cause
## 根本原因

All of this – the memoization cascade, the React Compiler, the performance footguns – stems from one JavaScript design decision: reference equality for functions, objects, and arrays.

所有这些问题——记忆化级联、React 编译器、性能陷阱——都源于一个 JavaScript 设计决策：函数、对象和数组的引用相等性。

If JavaScript had structural equality by default, a memoized React component could just check if the new props equal the old props, and skip re-rendering if they do. No `useCallback`, no `useMemo`, no compiler magic.

如果 JavaScript 默认有结构相等性，一个记忆化的 React 组件只需检查新 props 是否等于旧 props，如果相等就跳过重新渲染。不需要 `useCallback`，不需要 `useMemo`，不需要编译器魔法。

Instead, we have increasingly complex tools to work around a language feature that I've almost never seen anyone actually want. When was the last time you _needed_ to check if two variables pointed to the exact same array in memory, rather than arrays with the same contents?

相反，我们有越来越复杂的工具来解决一个我几乎从未见过有人真正想要的语言特性。你上一次*需要*检查两个变量是否指向内存中完全相同的数组，而不是具有相同内容的数组是什么时候？

Until JavaScript gets real equality comparison (I think it won't, the tuples and records proposal was [withdrawn](https://github.com/tc39/proposal-record-tuple/issues/394)), we're stuck with this.

在 JavaScript 获得真正的相等性比较之前（我认为不会了，tuples 和 records 提案已经被[撤回](https://github.com/tc39/proposal-record-tuple/issues/394)），我们只能忍受这个问题。

---

## My Suggestion?
## 我的建议？

In my free时间，I've been experimenting with a different approach: React for the UI layer and Rust (compiled to WebAssembly) for everything else. The Rust side handles all the actual logic while React becomes just a thin presentation layer.

在我的空闲时间，我一直在尝试一种不同的方法：React 用于 UI 层，Rust（编译为 WebAssembly）用于其他一切。Rust 端处理所有实际的业务逻辑，而 React 只是一个薄薄的展示层。

This setup lets me skip most of JavaScript's bullshit. The only thing I have to think about in JavaScript is React and UI stuff, because none of my actual business logic lives there. It's all in Rust.

这种设置让我可以跳过大部分 JavaScript 的废话。我在 JavaScript 中唯一需要考虑的是 React 和 UI 相关的东西，因为我所有的实际业务逻辑都不在那里。它都在 Rust 中。

Since I don't have much time to work on this project, I try to be conscious of where I'm spending my time in it. And because in this project I'm constantly switching between the two languages, I've developed a pretty intuitive feel for which one I'm more productive in. And I can say without hesitation: I feel about 10x more productive in Rust, precisely because I'm not fighting the language all the time. (Honestly, I feel like having a functioning `==` operator is pretty table stakes for a language that wants to be productive to work on, so it's surprising how many languages get this wrong.)

由于我没有太多时间在这个项目上工作，我努力注意我在哪里花费时间。因为在这个项目中我不断在两种语言之间切换，我对哪种语言让我更有生产力有了相当直观的感受。我可以毫不犹豫地说：我在 Rust 中感觉生产力提高了约 10 倍，正是因为我不需要一直与语言作斗争。（老实说，我觉得拥有一个正常工作的 `==` 运算符对于一种想要提高生产力的语言来说是很基本的要求，所以令人惊讶的是有那么多语言在这方面搞错了。）

It might take slightly longer to get an initial prototype on screen with Rust, compared to if it was all in JS. But the amount of time I spend in JavaScript debugging weird double renders, tracking down performance hiccups, or figuring out why my `useEffect` is running over and over? It's so extreme that I regret every second I spend writing JavaScript and wish I could write the whole thing in Rust. Read [this comment](https://news.ycombinator.com/item?id=45043929) for more details and a simple theoretical model for why Rust should be more productive than javascript in the medium term.

与全部用 JS 编写相比，用 Rust 获得初始原型可能需要稍微长一点时间。但我在 JavaScript 中调试奇怪的双重渲染、追踪性能问题或弄清楚为什么我的 `useEffect` 不断运行所花费的时间？这太夸张了，以至于我后悔花在写 JavaScript 上的每一秒，希望我能全部用 Rust 来写。阅读[这条评论](https://news.ycombinator.com/item?id=45043929)了解更多细节和一个简单的理论模型，解释为什么 Rust 在中期应该比 JavaScript 更有生产力。

Unfortunately, options for writing websites entirely in Rust are not quite ready at the moment. But I'm convinced that eventually someone will crack it and create a truly ergonomic way of writing websites in Rust. When that happens, I might never write JavaScript again.

不幸的是，完全用 Rust 编写网站的选项目前还不够成熟。但我相信最终有人会突破这个障碍，创造一种真正符合人体工程学的用 Rust 编写网站的方式。当那发生时，我可能再也不会写 JavaScript 了。

The app I'm referring to having built this way is [yap.town](https://yap.town). It's a language learning app I'm making to teach myself French (and I'm adding other languages as my friends request them). The entire course engine, spaced repetition system, and sync engine is all Rust. React just puts pixels on the screen based on what Rust tells it. It works pretty well in my opinion (and has allowed me to do some things that would be infeasible from a performance standpoint in JavaScript).

我用这种方式构建的应用是 [yap.town](https://yap.town)。这是一个语言学习应用，我做它是为了自学法语（而且我会根据朋友们的要求添加其他语言）。整个课程引擎、间隔重复系统和同步引擎都是 Rust。React 只是根据 Rust 告诉它的内容把像素放到屏幕上。在我看来这工作得相当好（而且让我能够做一些从性能角度来看在 JavaScript 中不可行的事情）。

(Of course, if you go this route you then have to write Rust, which brings its own problems. It's not my favorite language, but I'm not sure that there's a better non-JavaScript option for deploying to the web, just because of the fact that Rust doesn't need a heavy runtime.)

（当然，如果你走这条路，那你就得写 Rust，这会带来它自己的问题。它不是我最喜欢的语言，但我不确定是否有更好的非 JavaScript 选项用于部署到 Web，仅仅因为 Rust 不需要一个沉重的运行时。）

---

## 批判性思考评论

### 关于作者观点的反思

作者提出的核心观点——JavaScript 的引用相等性是导致 React 性能陷阱的根本原因——确实切中了现代前端开发的一个痛点。这种设计决策确实在日常开发中造成了大量的认知负担和潜在 bug。

然而，我认为作者的观点也存在一些可以商榷的地方：

**1. 结构相等性真的就是银弹吗？**

作者假设如果 JavaScript 有结构相等性，所有问题都会消失。但结构相等性也有其代价：
- 深度比较大型对象的开销可能很高
- 循环引用的处理会变得复杂
- 对于某些场景（如身份验证、缓存键），引用相等性确实是有意义的

**2. React 的设计哲学**

React 选择依赖数组和显式记忆化，某种程度上是一种"显式优于隐式"的设计哲学。虽然这增加了样板代码，但也让开发者清楚地知道什么时候会发生什么。完全自动的结构相等性比较可能会隐藏性能问题，让开发者失去对渲染行为的控制。

**3. Rust + React 的架构是否真的解决了问题？**

作者提到的 Rust + React 架构确实有趣，但这种架构也有其复杂性：
- 跨语言边界的数据传递开销
- 开发工具的复杂性增加
- 团队需要掌握两种语言

而且，Rust 本身也不是没有复杂性——借用检查器、生命周期管理等都需要相当的学习曲线。

**4. 对现代 React 生态的忽视**

文章似乎忽略了 React 18+ 的并发特性和新的响应式原语（如 useSignal 等），这些新特性在某种程度上正在缓解作者提到的问题。

**5. 实用主义的角度**

虽然理论上 JavaScript 的相等性设计有缺陷，但在实践中，大多数 React 应用并不会因为这个问题而崩溃。现代开发工具（如 React DevTools Profiler）和最佳实践已经很好地缓解了这些问题。

### 结论

作者的观点提供了一个有价值的视角，让我们重新审视 JavaScript 和 React 的一些设计决策。然而，技术选择总是权衡的结果。完全否定 JavaScript 转向 Rust 可能是一种过度反应。更务实的做法可能是：

1. 在性能关键的场景考虑使用 WebAssembly
2. 利用 React Compiler 等工具自动处理记忆化
3. 关注 TC39 的新提案，如 Records & Tuples（虽然被撤回，但类似概念可能会以其他形式回归）

技术的发展是渐进的，而不是革命的。理解问题的根源很重要，但解决方案往往需要在现有生态中寻找平衡点。

---

*原文链接：https://chadnauseam.com/coding/pltd/react-is-good-javascript-is-the-problem*
