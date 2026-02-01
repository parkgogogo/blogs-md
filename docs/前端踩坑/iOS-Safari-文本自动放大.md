#frontend #pitfall #ios

## iOS Safari 文本自动放大导致按钮换行

移动端 Safari 会在“可读性不足”时对文本自动放大，导致局部文字突然变大、换行。桌面端不会触发，所以很难本地复现。

### 观察
- 只在 iOS Safari 出现
- 文案突然变大，且在按钮内换行
- 同样的 CSS 在桌面端正常

### 推断：iOS 的 text autosizing 介入
当文本字号过小、letter-spacing 较大或布局过紧时，Safari 会在渲染阶段放大字体以保证可读性。
放大后文本宽度变大，于是触发换行；再叠加 `letter-spacing`，效果更明显。

### 最小修复
目标：禁止自动放大 + 防止换行 + 稳定行高。

```css
.daily-sentence-audio {
  white-space: nowrap;
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}

.daily-sentence-audio-label {
  line-height: 1;
  display: inline-block;
  font-size: 0.65rem; /* 可选 */
}
```

### 为什么桌面不复现
桌面 Safari/Chromium 不会做 text autosizing，所以不会出现“凭空变大”的现象。

### 小结
遇到“只在 iOS Safari 出现的文字变大/换行”，优先怀疑 text autosizing，别急着改布局。
