URL: https://devblogs.microsoft.com/oldnewthing/20260223-00/?p=112080

Last time, we saw that [Get­Async­Key­State is not the way to detect whether the ESC key was down at the time the current input message was generated](https://devblogs.microsoft.com/oldnewthing/20260220-00/?p=112074). But what about if we switched to Get­Key­State? Would that allow us to distinguish between an IDCANCEL caused by the ESC and an IDCANCEL that come from the Close button?

上次我们了解到，[GetAsyncKeyState 并不是检测当前输入消息生成时 ESC 键是否按下的正确方法](https://devblogs.microsoft.com/oldnewthing/20260220-00/?p=112074)。但如果我们改用 GetKeyState 呢？这样能否区分由 ESC 键引起的 IDCANCEL 和来自关闭按钮的 IDCANCEL？

It helps, in that it tells you whether the ESC key was down when the event occurred, but just because the ESC is down doesn’t mean that the ESC key is why you got the message.

它确实有帮助，因为它能告诉你事件发生时 ESC 键是否被按下，但仅仅因为 ESC 键处于按下状态，并不意味着这就是你收到该消息的原因。

For example, suppose your policy is to simply ignore the ESC key, but to close the dialog if the user clicks the Close button. If the user holds the ESC key and clicks the Close button, the initial press of the ESC will generate an IDCANCEL, and your call to Get­Key­State will report that the ESC is down, so you will ignore the message.

例如，假设你的策略是简单地忽略 ESC 键，但当用户点击关闭按钮时关闭对话框。如果用户按住 ESC 键并点击关闭按钮，ESC 键的初始按下会生成一个 IDCANCEL，而你对 GetKeyState 的调用会报告 ESC 键处于按下状态，因此你会忽略该消息。

And then the next IDCANCEL comes in due to the Close button, and your call to Get­Key­State will correctly report "The ESC key is still down." So your function says, "Oh, this came from the ESC key, so ignore it."

然后由于关闭按钮触发了下一个 IDCANCEL，而你对 GetKeyState 的调用会正确地报告"ESC 键仍处于按下状态"。于是你的函数会说："哦，这个来自 ESC 键，所以忽略它。"

Except that it didn’t come from the ESC key. It came from the Close button. It just so happens that the ESC is down, but that’s not the reason why you got the second IDCANCEL.

但实际上它并非来自 ESC 键，而是来自关闭按钮。只是碰巧 ESC 键处于按下状态，但这并不是你收到第二个 IDCANCEL 的原因。

Suppose you have a kiosk in a room with two entrances, a back entrance and a front entrance. If someone enters from the front door, you want to call the receptionist, but you don’t want to do it if they enter from the back door. What we’re doing by checking the ESC key is saying, "If the back door is open, then don’t call the receptionist." But it’s possible that somebody is just standing in the back doorway, holding the door open, and during that time, somebody comes in the front door. Your logic sees that the back door is open and suppresses the call to the receptionist because you had assumed that only one门 can be open at a time.

假设你有一个房间里的自助服务亭，房间有两个入口：后门和正门。如果有人从前门进入，你想呼叫接待员，但如果他们从后门进入，你就不想这么做。我们通过检查 ESC 键所做的事情相当于在说："如果后门开着，就不要呼叫接待员。"但有可能有人只是站在后门门口，把门敞开，而在此期间，有人从前门进来了。你的逻辑看到后门是开着的，就抑制了对接待员的呼叫，因为你之前假设一次只能有一扇门是开着的。

Next time, we’ll look at distinguishing ESC from Close.

下次，我们将探讨如何区分 ESC 键和关闭按钮。

## Author

Raymond has been involved in the evolution of Windows for more than 30 years. In 2003, he began a Web site known as The Old New Thing which has grown in popularity far beyond his wildest imagination, a development which still gives him the heebie-jeebies. The Web site spawned a book, coincidentally also titled The Old New Thing (Addison Wesley 2007). He occasionally appears on the Windows Dev Docs Twitter account to tell stories which convey no useful information.

## 作者简介

Raymond 参与 Windows 的演进已有 30 多年。2003 年，他创办了一个名为 "The Old New Thing" 的网站，其受欢迎程度远超他的想象，这一发展至今仍让他感到忐忑不安。该网站催生了一本书，巧合的是书名也叫《The Old New Thing》（Addison Wesley 2007 年出版）。他偶尔会在 Windows Dev Docs Twitter 账户上出现，讲述一些没有任何实用信息的故事。

---

## 批判性思考评论

这篇文章展示了 Raymond Chen 在 Windows 编程领域深厚的经验和对细节的极致追求。通过一个简单的技术问题——如何区分 ESC 键和关闭按钮触发的 IDCANCEL 消息——作者揭示了异步输入处理中的一个常见陷阱。

**关键洞察：**
1. **状态检测的局限性**：GetKeyState 虽然能告诉你按键的当前状态，但无法建立因果关系。这类似于编程中常见的"相关性不等于因果性"问题。

2. **类比的力量**：作者用"房间有两个门"的类比非常精妙，将抽象的消息队列问题转化为直观的场景，让读者更容易理解并发/异步状态下的逻辑陷阱。

3. **工程思维的体现**：好的工程师不仅要让代码"能工作"，还要考虑边界情况和意外场景。这篇文章展示了为什么简单的解决方案往往不足以应对复杂的用户交互场景。

**反思：** 在 GUI 编程中，我们常常假设用户的操作是顺序的、原子化的，但现实中用户可能同时执行多个操作（如按住一个键的同时点击鼠标）。这种"组合输入"的场景是许多 bug 的来源。文章提醒我们，在处理用户输入时，必须考虑状态的时序性和真正的事件源，而不仅仅是检查某个状态标志。
