#frontend #safari #webkit #rendering #pitfall

## Safari 的「残影」不是样式问题

有些 UI 问题看起来像样式错了，实际上是渲染层没刷新。这篇记录一个 Safari 上典型的“残影”案例，以及我如何确认它不是布局问题。

### 观察（用类比理解）
把它想象成拍照时的“拖影”：上一帧的影子没擦干净，叠到了下一帧。

更具体一点：
- 只在“状态切换”的那一瞬出现
- 只在 Safari 上出现
- 任意一次交互就消失

这种“来得快、走得快”的问题，优先怀疑重绘/合成层，而不是布局。

### 推断：Safari 的重绘/合成层残影
Safari 在某些 flex + border 场景下，会把上一帧的边框像素残留到下一帧。
所以你看到“多出来的线条”，但它其实只是旧像素残留。

### 最小修复：强制重建局部 DOM
目标：不改视觉、不改布局，只让 Safari 必须重绘。

```tsx
<div
  key={`word-actions-${data.status ?? 'unknown'}`}
  className="flex flex-wrap items-center justify-between gap-2 mb-3"
>
  ...
</div>
```

`key` 绑定状态后，React 在状态切换时重建这一行 DOM，Safari 必然重新绘制。

### 为什么不是“改样式”
“去掉边框”只是绕开问题，并不能保证下一次不会在别处复现。更重要的是：
- 其他浏览器本来没问题，改样式会引入视觉回归
- 根因仍是 Safari 的重绘残影

修复策略应该是：让 Safari 不可能复用旧像素。

### 备选方案
1) 强制重建 DOM（推荐，改动小）
2) 给容器加 `transform: translateZ(0)` 进入独立合成层
3) 状态切换时短暂加/删一个 class 触发 repaint

### 小结
如果 UI 问题满足：
- 只在 Safari 出现
- 一次交互立刻消失

优先怀疑重绘残影，不要立刻大改布局。最稳妥的办法是强制重绘或重建局部 DOM。
