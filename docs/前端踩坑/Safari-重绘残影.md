#frontend #safari #webkit #rendering #pitfall

# Safari 的「残影」不是样式问题

一次很典型的 UI 幻觉：样式看起来错了，但 DOM 没问题。

---

# 观察
可以把它想象成拍照时的“拖影”：上一帧的影子没被擦干净，叠到下一帧。

更具体一点：
- 只有在“状态切换”的那一瞬出现
- 只在 Safari 上出现
- 做任意一次交互（比如切 Tab）就消失

这种“来得快、走得快”的问题，通常不是布局错了，而是渲染层没有重绘。

---

# 推断：Safari 的重绘/合成层残影
Safari 在某些 flex + border 场景下，会把上一帧的边框像素残留到下一帧。
于是你会看到“多出来的线条”，但它其实只是旧像素。

---

# 最小修复：强制重建局部 DOM
目标：**不改视觉，不改布局，只让 Safari 必须重绘**。

```tsx
<div
  key={`word-actions-${data.status ?? 'unknown'}`}
  className="flex flex-wrap items-center justify-between gap-2 mb-3"
>
  ...
</div>
```

`key` 绑定状态后，React 在状态切换时重建这一行 DOM，Safari 必然重新绘制。

---

# 为什么不是“改样式”
“去掉边框”只是绕开问题，并不能保证下一次不会在别处复现。更重要的是：
- 其他浏览器本来没问题，改样式会引入视觉回归
- 根因仍是 Safari 的重绘残影

**修复策略应该是：让 Safari 不可能复用旧像素。**

---

# 备选方案（侵入度从低到高）
1) **强制重建 DOM**（推荐，改动小）
2) 给容器加 `transform: translateZ(0)`，进入独立合成层
3) 状态切换时短暂加/删一个 class，触发 repaint

---

# 小结
如果 UI 问题满足：
- 只在 Safari 出现
- 一次交互立刻消失

优先怀疑 **重绘残影**，不要立刻大改布局。最稳妥的办法是 **强制重绘或重建局部 DOM**。
