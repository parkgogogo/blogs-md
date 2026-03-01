# From Noise to Image – interactive guide to diffusion
# 从噪声到图像——扩散模型交互式指南

**Original URL:** https://lighthousesoftware.co.uk/projects/from-noise-to-image/  
**Author:** Steve Anderson  
**Date:** 10th Feb 2026

---

## How many possible images are there?
## 有多少种可能的图像？

**EN:** Our universe has about 10^80 atoms. Now imagine if each atom contained its own universe, with 10^80 atoms inside. Even that barely scratches the surface. You'd need about 5,000 layers of atom-universes, nested one inside the next, before you reached the number of possible images the size of the one above - about 10^400,000. That's a 1 with 400,000 zeroes after it.

**CN:** 我们的宇宙大约有 10^80 个原子。现在想象一下，如果每个原子都包含它自己的宇宙，里面又有 10^80 个原子。即便如此，这还只是冰山一角。你需要大约 5,000 层原子宇宙，一层嵌套在另一层里面，才能达到上面那张图像大小的所有可能图像数量——大约是 10^400,000。那是 1 后面跟着 40 万个零。

**EN:** As you can imagine, the vast majority of these are nothing but random noise. Depending on your computer, you're seeing up to 60 random images per second. If you see anything that looks like a real image before the heat death of the universe, let me (or my descendants) know.

**CN:** 你可以想象，绝大多数这些图像只不过是随机噪声。取决于你的电脑性能，你每秒能看到多达 60 张随机图像。如果你在宇宙热寂之前看到任何看起来像真实图像的东西，请告诉我（或我的后代）。

**EN:** Amazingly, diffusion models can navigate this vast space of possibilities to produce coherent results. Unlike humans who start with a blank canvas and add paint, diffusion models start with random noise, and gradually remove the noise until an image emerges.

**CN:** 令人惊讶的是，扩散模型能够在这个广阔的可能性空间中找到方向，生成连贯的结果。与人类从空白画布开始添加颜料不同，扩散模型从随机噪声开始，然后逐渐去除噪声，直到图像浮现。

---

## A smaller world
## 一个更小的世界

**EN:** Actually it's not as bad as I made out, because the model operates in a compressed, lower-dimensional space called *latent space*. During training, the model is trained together with an encoder/decoder that can translate from this latent space to real images. In these examples, the latent space has 12x fewer dimensions than the full image space - still vast, but more manageable.

**CN:** 实际上并没有我说的那么糟糕，因为模型在一个被称为**潜空间（latent space）**的压缩低维空间中运作。在训练过程中，模型与一个编码器/解码器一起训练，后者可以将潜空间转换为真实图像。在这些例子中，潜空间的维度比完整图像空间少 12 倍——虽然仍然巨大，但更容易管理。

**EN:** We can't show the full latent space because it has too many dimensions, but I've compressed it down to give you a feel for it. From here on, we ignore the latent space and show the fully decoded image at each step - because it's easier for humans to understand. But in reality, the decoding only happens right at the end.

**CN:** 我们无法展示完整的潜空间，因为它有太多维度，但我将其压缩以让你感受一下。从现在开始，我们忽略潜空间，展示每一步完全解码后的图像——因为这样对人类来说更容易理解。但实际上，解码只在最后一步发生。

---

## Where words live
## 词语居住的地方

**EN:** Just like the multi-dimensional space of possible images, text prompts can be mapped to a high-dimensional "embedding space". Each prompt lives at a particular spot in this space, and similar prompts cluster together.

**CN:** 就像可能图像的多维空间一样，文本提示词可以被映射到一个高维的**嵌入空间（embedding space）**。每个提示词都存在于这个空间中的一个特定位置，相似的提示词会聚集在一起。

**EN:** Again, we can't show the full embedding because it's too high-dimensional but we can show this 2D compression. Notice how similar concepts group together. The embedding acts like a "compass" for the diffusion process. At each step on its journey, the model looks at the embedding to figure out the best direction to move.

**CN:** 同样，我们无法展示完整的嵌入，因为它的维度太高，但我们可以展示这个二维压缩版本。注意相似的概念是如何聚在一起的。嵌入就像扩散过程的**指南针**。在旅程的每一步，模型都会查看嵌入以确定最佳的移动方向。

---

## The starting point
## 起点

**EN:** If we start at different points in the possible-image space, we end up at slightly different destinations. This is determined by the *random seed* - a number that starts off the initial randomisation.

**CN:** 如果我们从可能图像空间中的不同点出发，最终会到达略有不同的目的地。这是由**随机种子（random seed）**决定的——一个启动初始随机化的数字。

**EN:** Different random seeds with the same prompt produce different but related images. Each seed represents a different starting point in the vast possibility space.

**CN:** 相同提示词下不同的随机种子会产生不同但相关的图像。每个种子代表在巨大可能性空间中的一个不同起点。

---

## Dividing the path
## 分割路径

**EN:** We can choose how many steps we take before stopping. A small number means we have to take big steps, and can end up off track - if we get there at all. But after a certain point, taking more steps doesn't help much, and just wastes time.

**CN:** 我们可以选择在停止前走多少步。步数太少意味着我们必须迈大步，可能会偏离轨道——如果最终能到达的话。但在某一点之后，增加步数帮助不大，只是浪费时间。

**EN:** Different numbers of inference steps: 4 steps, 12 steps, 28 steps, 42 steps. More steps generally lead to better results, but with diminishing returns.

**CN:** 不同的推理步数：4 步、12 步、28 步、42 步。更多的步骤通常会带来更好的结果，但收益递减。

---

## The weight of words
## 词语的重量

**EN:** A vague prompt leads to a more wobbly compass. More detailed prompts constrain the direction more tightly, leading to better results.

**CN:** 模糊的提示词会让指南针更不稳定。更详细的提示词能更严格地约束方向，从而产生更好的结果。

**EN:** Consider the progression:
- "A monarch butterfly"
- "A monarch butterfly on a purple coneflower, macro"
- "A monarch butterfly on a purple coneflower, macro close-up, delicate orange and black wing"
- "A monarch butterfly on a purple coneflower, macro close-up, delicate orange and black wing detail, morning dew, soft bokeh"

**CN:** 考虑这个递进：
- "一只帝王蝶"
- "一只帝王蝶在紫色锥花上，微距"
- "一只帝王蝶在紫色锥花上，微距特写，精致的橙色和黑色翅膀"
- "一只帝王蝶在紫色锥花上，微距特写，精致的橙色和黑色翅膀细节，晨露，柔和散景"

**EN:** Each additional word adds detail and constrains the possible outcomes, guiding the model more precisely toward the desired result.

**CN:** 每增加一个词都增加了细节并限制了可能的结果，更精确地引导模型朝向期望的结果。

---

## The space between words
## 词语之间的空间

**EN:** Because prompts also exist in their own "embedding space", we can follow a path between any two prompt embeddings, and generate images along the way. These "in-between" points don't correspond to human words, but they exist in the embedding space.

**CN:** 因为提示词也存在于它们自己的"嵌入空间"中，我们可以在任意两个提示词嵌入之间跟随一条路径，并在途中生成图像。这些"中间"点不对应人类语言中的词汇，但它们确实存在于嵌入空间中。

**EN:** For example, blending between:
- "A monarch butterfly on a purple coneflower, macro close-up, delicate orange and black wing detail, morning dew, soft bokeh"
- "A snail resting on a moss-covered rock, extreme close-up, shell spiral detail, rain droplets, rich green, soft overcast lighting"

**CN:** 例如，在两个提示词之间混合：
- "一只帝王蝶在紫色锥花上，微距特写，精致的橙色和黑色翅膀细节，晨露，柔和散景"
- "一只蜗牛栖息在苔藓覆盖的岩石上，超特写，贝壳螺旋细节，雨滴，浓郁的绿色，柔和阴天光线"

**EN:** At 33% blend, 66% blend - the images gradually transform from one concept to another, showing the continuous nature of the embedding space.

**CN:** 在 33% 混合、66% 混合时——图像逐渐从一个概念转变为另一个概念，展示了嵌入空间的连续性。

---

## The pull of the prompt
## 提示词的牵引力

**EN:** The model decides how strongly to follow your prompt using a number called the *guidance scale* (also known as CFG scale). A higher value gives the prompt a stronger "steering" effect, but if we set it too high we can end up with unnatural, oversaturated images.

**CN:** 模型使用一个称为**引导比例（guidance scale）**（也称为 CFG 比例）的数字来决定跟随提示词的强度。更高的值会给提示词更强的"引导"效果，但如果设置得太高，我们最终可能会得到不自然的、过度饱和的图像。

**EN:** Examples with different guidance scales:
- Guidance Scale = 1.0 (minimal guidance, more randomness)
- Guidance Scale = 5.5 (balanced)
- Guidance Scale = 10.5 (strong guidance)
- Guidance Scale = 15.0 (excessive guidance, oversaturated)

**CN:** 不同引导比例的示例：
- 引导比例 = 1.0（最小引导，更多随机性）
- 引导比例 = 5.5（平衡）
- 引导比例 = 10.5（强引导）
- 引导比例 = 15.0（过度引导，过度饱和）

**EN:** Finding the right balance is key - too low and the image drifts from the prompt; too high and the image becomes unnatural.

**CN:** 找到正确的平衡是关键——太低，图像会偏离提示词；太高，图像会变得不自然。

---

## The full journey
## 完整旅程

**EN:** Imagine you've been plonked in the middle of an unfamiliar terrain with an uncertain destination and nothing but a compass to guide you. You come up with the following plan:
- Check the compass
- Walk a bit in that direction
- Check the compass again
- Walk a bit in the new direction
- Repeat a fixed number of times

**CN:** 想象你被丢在一片陌生的地形中间，目的地不确定，只有一只指南针来引导你。你制定了以下计划：
- 查看指南针
- 朝那个方向走一段
- 再次查看指南针
- 朝新方向走一段
- 重复固定次数

**EN:** Diffusion models follow a very similar pattern, guided by these 4 things:

**CN:** 扩散模型遵循一个非常相似的模式，由以下 4 个因素引导：

**EN:** **Random seed** - where you start  
*Different starting points lead to slightly different destinations.*

**CN:** **随机种子**——你从哪里开始  
*不同的起点会导致略有不同的终点。*

**EN:** **Prompt** - the compass  
*A rickety old compass that only points "northish" will get you somewhere, but not necessarily where you want to be.*

**CN:** **提示词**——指南针  
*一个只能指向"北边大概方向"的摇摇欲坠的旧指南针会带你去某个地方，但不一定是你想去的地方。*

**EN:** **Step count** - how often you check the compass  
*Check the compass too rarely and you'll drift off course. But checking all the time will slow you down.*

**CN:** **步数**——你多久查看一次指南针  
*查看指南针太少，你会偏离航线。但一直查看会拖慢你的速度。*

**EN:** **Guidance scale** - how strongly you follow the compass  
*Blindly follow the compass, and you may end up stuck in a river. But ignore it completely, and you'll wander aimlessly.*

**CN:** **引导比例**——你跟随指南针的强度  
*盲目跟随指南针，你可能会被困在河里。但完全忽视它，你会漫无目的地游荡。*

---

## Conclusion
## 结论

**EN:** By combining these, the model navigates from pure chaos to a coherent image that matches your prompt. An AI model generating an image may look like magic, but now you know it's just navigation through an unimaginably vast space of possibilities.

**CN:** 通过结合这些因素，模型从纯粹的混沌导航到与提示词匹配的连贯图像。AI 模型生成图像看起来可能像魔法，但现在你知道了，这只是在难以想象的可能性空间中进行导航。

**EN:** Which, to be fair, is still super cool.

**CN:** 公平地说，这仍然超级酷。

---

## Thanks
## 致谢

**EN:** Thanks to [Photoroom](https://www.photoroom.com), who open sourced [their text-to-image model PRX](https://huggingface.co/blog/Photoroom/prx-open-source-t2i-model), allowing me to generate all of these examples. All examples were generated using the [Photoroom/prx-256-t2i-sft](https://huggingface.co/Photoroom/prx-256-t2i-sft) model. Extra thanks to [Jon Almazán](https://huggingface.co/jon-almazan) for the support and ideas.

**CN:** 感谢 [Photoroom](https://www.photoroom.com) 开源了[他们的文生图模型 PRX](https://huggingface.co/blog/Photoroom/prx-open-source-t2i-model)，使我能够生成所有这些示例。所有示例都使用 [Photoroom/prx-256-t2i-sft](https://huggingface.co/Photoroom/prx-256-t2i-sft) 模型生成。特别感谢 [Jon Almazán](https://huggingface.co/jon-almazan) 的支持和创意。

---

*Created by Steve Anderson, Founder of Lighthouse Software*

*由 Lighthouse Software 创始人 Steve Anderson 创作*
