URL: https://www.mariannefeng.com/portfolio/kindle/

# Hacking an old Kindle to display bus arrival times

# 破解旧Kindle显示公交到站时间

This is how I turned an old Kindle (Kindle Touch 4th Generation/K5/KT) into a live bus feed that refreshes every minute with the option to exit out of dashboard mode by pressing the menu button. It's basically [TRMNL](https://trmnl.com/) without the $140 price tag.

这是我把一台旧Kindle（Kindle Touch第四代/K5/KT）改造成实时公交信息显示屏的过程，它每分钟刷新一次，还可以通过按下菜单按钮退出仪表盘模式。这基本上就是[TRMNL](https://trmnl.com/)，但不需要花140美元。

The high level steps are:

高层次的步骤如下：

1. Jailbreak your kindle
2. Install KUAL & MRPI
3. Setup SSH
4. Run a server accessible over the internet (or locally) that serves the Kindle image
5. Create a KUAL app

1. 越狱你的Kindle
2. 安装KUAL和MRPI
3. 设置SSH
4. 运行一个可以通过互联网（或本地）访问的服务器，为Kindle提供图像
5. 创建一个KUAL应用

## 1. Jailbreaking your Kindle

## 1. 越狱你的Kindle

This will be your [Kindle hacking bible](https://www.mobileread.com/forums/showthread.php?t=225030) for steps 1 - 3. You need to figure out what version of Kindle you have, its firmware version (shorthand FW in the Kindle forum guides + readmes), download the appropriate tar file and follow jailbreak instructions.

这将是你在步骤1-3中的[Kindle破解圣经](https://www.mobileread.com/forums/showthread.php?t=225030)。你需要弄清楚你拥有哪个版本的Kindle，它的固件版本（在Kindle论坛指南和readme中简称为FW），下载适当的tar文件并按照越狱说明操作。

Once you've successfully jailbroken your Kindle, it's time to install some things.

成功越狱Kindle后，就该安装一些东西了。

## 2. Installing KUAL & MRPI

## 2. 安装KUAL和MRPI

KUAL is a custom Kindle app launcher. MRPI allows us to install custom apps onto the Kindle (you may not need MRPI if you have a newer Kindle). This part was frustrating - reading through forum threads gives me a headache. The most helpful resource I found was the [Kindle modding wiki](https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi). Maybe other people aren't as oblivious as me but it took me half a day to realize that the "next step" in each guide can be accessed by clicking the "Next Step" button at the bottom of the page.

KUAL是一个自定义Kindle应用启动器。MRPI允许我们在Kindle上安装自定义应用（如果你有较新的Kindle，可能不需要MRPI）。这部分让人沮丧——阅读论坛帖子让我头疼。我发现最有用的资源是[Kindle改装维基](https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi)。也许其他人不像我这么迟钝，但我花了半天时间才意识到每个指南中的"下一步"可以通过点击页面底部的"Next Step"按钮来访问。

A gotcha for me was that I *had* to follow the Setting up a Hotfix guide *before* attempting to install KUAL & MRPI.

对我来说一个需要注意的点是，我*必须*在尝试安装KUAL和MRPI之前先按照设置Hotfix的指南操作。

After successfully installing KUAL & MRPI, I also [Disabled OTA Updates](https://kindlemodding.org/jailbreaking/post-jailbreak/disable-ota.html) because why not. I didn't follow any other guides in the Kindle Modding wiki after disabling OTA Updates because they didn't seem relevant.

成功安装KUAL和MRPI后，我还[禁用了OTA更新](https://kindlemodding.org/jailbreaking/post-jailbreak/disable-ota.html)，因为为什么不呢。禁用OTA更新后，我没有按照Kindle改装维基中的其他指南操作，因为它们似乎不相关。

## 3. Setup SSH for your Kindle

## 3. 为你的Kindle设置SSH

This can be done with a KUAL extension called USBNetwork (downloadable from the [Kindle hacking bible](https://www.mobileread.com/forums/showthread.php?t=225030)) that will allow you to SSH onto your Kindle as if it were a regular server.

这可以通过一个名为USBNetwork的KUAL扩展来完成（可从[Kindle破解圣经](https://www.mobileread.com/forums/showthread.php?t=225030)下载），它可以让你像访问普通服务器一样通过SSH连接到你的Kindle。

However, nowhere in the forums could I find any information about how to actually install a KUAL extension using MRPI. Finally, this helpful [blogpost on setting up SSH for Kindle](https://blog.znjoa.com/2023/07/26/installing-usbnetwork-on-kindle/) came to the rescue. I followed the steps that explained to how to install the extension and how to setup SSH via USB. I ignored the rest of the instructions on the page because I'm not concerned about adding a password to the Kindle or setting up SSH over wifi.

然而，我在论坛中找不到任何关于如何使用MRPI实际安装KUAL扩展的信息。最后，这篇有用的[关于为Kindle设置SSH的博客文章](https://blog.znjoa.com/2023/07/26/installing-usbnetwork-on-kindle/)救了我。我按照解释如何安装扩展以及如何通过USB设置SSH的步骤操作。我忽略了页面上其余的说明，因为我不关心为Kindle添加密码或通过WiFi设置SSH。

If you've setup SSH successfully, when the Kindle is plugged in, your computer's network tab should have a new item in 'Connected' mode:

如果你成功设置了SSH，当Kindle插入时，你电脑的网络标签页应该在"已连接"模式下有一个新项目：

Here's what my successfully connected Kindle looks like in the network settings tab:

这是我成功连接的Kindle在网络设置标签页中的样子：

Congratulations! Your Kindle is now ready to run custom code.

恭喜！你的Kindle现在可以运行自定义代码了。

## 4. Running a server that generates an image for the Kindle

## 4. 运行一个为Kindle生成图像的服务器

How displaying custom data on the Kindle works is that we need to create a png that fits the Kindle resolution, then draw the image onto the Kindle itself.

在Kindle上显示自定义数据的工作原理是，我们需要创建一个适合Kindle分辨率的png，然后将图像绘制到Kindle本身。

Since I live in New Jersey, I wanted to display NJTransit bus times on my Kindle. Luckily, NJTransit has a public GraphQL server that returns bus arrival times for any stop number.

由于我住在新泽西，我想在我的Kindle上显示NJTransit公交时间。幸运的是，NJTransit有一个公共GraphQL服务器，可以返回任何站点的公交到达时间。

### Pulling NJ Transit bus data

### 获取NJ Transit公交数据

After poking around in the network tab of the [NJ Transit Bus Website](https://www.njtransit.com/bus-to), I found this GraphQL query that returns the bus number, arrival time, current capacity, destination, and departing time in minutes:

在[NJ Transit公交网站](https://www.njtransit.com/bus-to)的网络标签页中摸索后，我找到了这个GraphQL查询，它可以返回公交车号、到达时间、当前容量、目的地和距离发车还有多少分钟：

```
  query BusArrivalsByStopID($stopID: ID!) {
    getBusArrivalsByStopID(stopID: $stopID) {
      departingIn
      destination
      route
      time
      capacity
      __typename
    }
  }
```

If you're also a Jersey girl, you can run the following curl to get upcoming bus times (don't forget to replace YOUR_STOP_NUMBER):

如果你也是新泽西女孩，你可以运行以下curl命令来获取即将到来的公交时间（别忘了替换YOUR_STOP_NUMBER）：

```
curl 'https://www.njtransit.com/api/graphql/graphql' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  --data-raw $'{"operationName":"BusArrivalsByStopID","variables":{"stopID":"YOUR_STOP_NUMBER"},"query":"query BusArrivalsByStopID($stopID: ID\\u0021) {\\n  getBusArrivalsByStopID(stopID: $stopID) {\\n    departingIn\\n    destination\\n    busID\\n    route\\n    time\\n    vehicleID\\n    capacity\\n    __typename\\n  }\\n}"}'
```

### Creating a server

### 创建服务器

In the majority of the guides I read during this process (two most helpful being [Matt Healy's Kindle Dashboard guide](https://matthealy.com/kindle) and [Hemant's Kindle Dashboard guide](https://terminalbytes.com/reviving-kindle-paperwhite-7th-gen)) they use puppeteer to convert HTML to png. This does not work for me because I'm cheap and have a single $6 Digital Ocean droplet that I use for all side projects. Every time I ran puppeteer on it the entire server shits itself.

在我阅读这个过程中的大多数指南时（最有帮助的两篇是[Matt Healy的Kindle仪表盘指南](https://matthealy.com/kindle)和[Hemant的Kindle仪表盘指南](https://terminalbytes.com/reviving-kindle-paperwhite-7th-gen)），他们使用puppeteer将HTML转换为png。这对我来说行不通，因为我很吝啬，只有一个6美元的Digital Ocean droplet用于所有副业项目。每次我在上面运行puppeteer时，整个服务器都会崩溃。

Instead I created an endpoint that formats the bus data into HTML, then the docker container that runs the server has a cron that runs the [wkhtmltoimage](https://wkhtmltopdf.org/) command to generate a new png every 3 minutes using the HTML endpoint. The server then serves the generated png file at a separate endpoint.

相反，我创建了一个端点，将公交数据格式化为HTML，然后运行服务器的docker容器有一个cron，每3分钟运行一次[wkhtmltoimage](https://wkhtmltopdf.org/)命令，使用HTML端点生成一个新的png。然后服务器在另一个端点提供生成的png文件。

Here's what the 2 relevant endpoints look like for my Kindle:

这是我的Kindle的两个相关端点的样子：

- [HTML endpoint used by wkhtmltoimage to generate an image](https://kindle.mariannefeng.com/html)
- [Endpoint used by the Kindle to retrieve the image](https://kindle.mariannefeng.com/screen)

- [wkhtmltoimage用来生成图像的HTML端点](https://kindle.mariannefeng.com/html)
- [Kindle用来获取图像的端点](https://kindle.mariannefeng.com/screen)

The entire server code - Dockerfile, scripts, the server itself - can be found in the [`server` folder of my Kindle hax repo](https://github.com/mariannefeng/kindle-hax/tree/main/server). It's written in Node because I was originally using Puppeteer before discovering the performance issues, but it'd be a fun optimization exercise to rewrite in Go.

整个服务器代码——Dockerfile、脚本、服务器本身——可以在我的[Kindle hax仓库的`server`文件夹](https://github.com/mariannefeng/kindle-hax/tree/main/server)中找到。它是用Node编写的，因为我最初在使用Puppeteer，后来才发现了性能问题，但用Go重写会是一个有趣的优化练习。

### Generating the image

### 生成图像

The most important thing is that the image needs to conform to your Kindle's screen resolution. You can find what yours is by running `eips -i` when SSH-ed into the Kindle. `eips` is the command you'll be using to display an image on your Kindle. I found this [eips menu guide helpful](https://wiki.mobileread.com/wiki/Eips)

最重要的是图像需要符合Kindle的屏幕分辨率。你可以通过SSH连接到Kindle时运行`eips -i`来找到你的分辨率。`eips`是你用来在Kindle上显示图像的命令。我发现这个[eips菜单指南很有帮助](https://wiki.mobileread.com/wiki/Eips)。

You'll see an output like this:

你会看到类似这样的输出：

My Kindle expects a 600x800 image and the image must be rotated. Without passing a rotate command during the image generation process, I got skewed images like this:

我的Kindle期望一个600x800的图像，而且图像必须旋转。如果在图像生成过程中不传递旋转命令，我会得到像这样的歪斜图像：

However, after rotating, the bus times could only be viewed horizontally and I wanted to mount my Kindle vertically. What that meant was I had to rotate the HTML itself. But when rotating an image then taking a snapshot, the rotation is around the screen中心 so the snapshot made by wkhtmltoimage kept on cutting off the bus times. Finally, a combination of rotate and translate gave me what I needed, which was a rotated image that was aligned to the top left of the screen:

然而，旋转后，公交时间只能水平查看，而我想垂直安装我的Kindle。这意味着我必须旋转HTML本身。但是当旋转图像然后拍摄快照时，旋转是围绕屏幕中心进行的，所以wkhtmltoimage制作的快照不断切断公交时间。最后，旋转和平移的组合给了我我需要的东西，即一个旋转的图像，对齐到屏幕的左上角：

```
transform: rotate(90deg) translateX(-100px) translateY(-100px);
```

Once you have a server with an endpoint that serves your image, you're ready for the last step.

一旦你有一个带有提供图像端点的服务器，你就准备好进行最后一步了。

## 5. Creating a KUAL app

## 5. 创建KUAL应用

Going into this, I wanted two things - an easy way to exit dashboard mode and a relatively up to date bus schedule. All the guides I've seen thus far ran a cron on their Kindle that hit their endpoint at a specified interval. However I didn't like this because I didn't want the Kindle to always run the dashboard after restarts. I want to control when the dashboard is displayed and that meant creating a custom KUAL app.

开始这个项目时，我想要两样东西——一种轻松退出仪表盘模式的方法，以及一个相对最新的公交时刻表。迄今为止我看到的所有指南都在他们的Kindle上运行cron，以指定间隔访问他们的端点。然而我不喜欢这样，因为我不希望Kindle在重启后总是运行仪表盘。我想控制何时显示仪表盘，这意味着要创建一个自定义KUAL应用。

The general layout is:

一般布局是：

```
bin/ # executable scripts here
menu.json # controls the menu items in the KUAL dashboard
config.xml # no clue wtf this is
```

```
bin/ # 可执行脚本放在这里
menu.json # 控制KUAL仪表盘中的菜单项
config.xml # 不知道这是什么鬼
```

Whiled SSH-ed into your Kindle, place your custom extension folder inside of `/mnt/us/extensions/`. If you used [my custom dash code](https://github.com/mariannefeng/kindle-hax/tree/main/kindle), after restarting and launching KUAL, you'll see your custom extension listed in KUAL and after clicking into it, a single menu item titled 'Start dashboard':

通过SSH连接到你的Kindle时，将你的自定义扩展文件夹放在`/mnt/us/extensions/`中。如果你使用了[我的自定义仪表盘代码](https://github.com/mariannefeng/kindle-hax/tree/main/kindle)，重启并启动KUAL后，你会在KUAL中看到你的自定义扩展，点击进入后，会有一个标题为"Start dashboard"的单一菜单项：

### The dashboard start script explained

### 仪表盘启动脚本解释

When you press 'Start dashboard', you can see in the [menu.json](https://github.com/mariannefeng/kindle-hax/blob/main/kindle/custom-dash/menu.json) that bin/start.sh will execute. The [start script](https://github.com/mariannefeng/kindle-hax/blob/main/kindle/custom-dash/bin/start.sh) has comments explaining what it does. Some interesting things I've never worked with before:

当你按下"Start dashboard"时，你可以在[menu.json](https://github.com/mariannefeng/kindle-hax/blob/main/kindle/custom-dash/menu.json)中看到bin/start.sh将会执行。[启动脚本](https://github.com/mariannefeng/kindle-hax/blob/main/kindle/custom-dash/bin/start.sh)有注释解释它的作用。一些我以前从未用过的有趣的东西：

```
# ignore HUP since kual will exit after pressing start, and that might kill our long running script
trap '' HUP
...
# ignore term since stopping the framework/gui will send a TERM signal to our script since kual is probably related to the GUI
trap '' TERM
...
trap - TERM
```

```
# 忽略HUP，因为kual会在按下开始后退出，这可能会终止我们的长运行脚本
trap '' HUP
...
# 忽略term，因为停止框架/gui会向我们的脚本发送TERM信号，因为kual可能与GUI相关
trap '' TERM
...
trap - TERM
```

trap! Here's a [helpful resource explaining the bash trap command](https://www.linuxjournal.com/content/bash-trap-command). The TL;DR of it is that without ignoring certain signals, the script will always early exit.

trap！这是一篇[解释bash trap命令的有用资源](https://www.linuxjournal.com/content/bash-trap-command)。简单来说，如果不忽略某些信号，脚本总是会提前退出。

Getting rtcwake to work was also annoying. For me, calling rtcwake on the default device (skipping `-d` flag) never worked, I had to list possible devices then choose a different one. The one that reacted to the rtcwake command was `rtc1` for me

让rtcwake工作也很烦人。对我来说，在默认设备上调用rtcwake（跳过`-d`标志）永远不起作用，我必须列出可能的设备然后选择一个不同的。对我的设备来说，响应rtcwake命令的是`rtc1`。

```
do_night_suspend() {
  sync
  rtcwake -d rtc1 -m mem -s "$WAKE_IN_SECONDS"
}
```

The `refresh_screen` function is important. This is the whole reason we did all that server and image generation stuff earlier. It retrieves an image at an endpoint, clears the screen twice, draws the image from the server and positions it slightly lower on the screen to make room for the status bar up top. The last line displays the datetime, wifi status, and battery remaining.

`refresh_screen`函数很重要。这正是我们之前做所有服务器和图像生成工作的全部原因。它从端点获取图像，清除屏幕两次，从服务器绘制图像并将其定位在屏幕稍低的位置，为顶部的状态栏留出空间。最后一行显示日期时间、WiFi状态和剩余电量。

```
refresh_screen() {
  curl -k "$SCREEN_URL" -o "$DIR/screen.png"
  eips -c
  eips -c
  eips -g "$DIR/screen.png" -x 0 -y 30 -w gc16
  # Draw date/time and battery at top (eips can't print %, so we strip it from gasgauge-info -c)
  eips 1 1 "$(TZ=EST5EDT date '+%Y-%m-%d %I:%M %p') - wifi $(cat /sys/class/net/wlan0/operstate 2>/dev/null || echo '?') - battery: $(gasgauge-info -c 2>/dev/null | sed 's/%//g' || echo '?')"
}
```

This part of the script listens for the user pressing the menu button.

脚本的这部分监听用户按下菜单按钮。

```
script -q -c "evtest /dev/input/event2 2>&1" /dev/null | grep -m 1 -q "code 102 (Home), value 1" && "$DIR/stop.sh"
```

`evtest` is the command that worked for me for listening for incoming events on a specified device on the kindle. In my case, any time I pressed the menu button, the evtest command outputs `code 102 (Home), value 1`.

`evtest`是对我有用的命令，用于监听Kindle上指定设备的传入事件。对我来说，每次我按下菜单按钮时，evtest命令都会输出`code 102 (Home), value 1`。

When the user presses the menu button, the [stop.sh script](https://github.com/mariannefeng/kindle-hax/blob/main/kindle/custom-dash/bin/stop.sh) is called automatically, which will kill the dashboard, clear the screen, and restart the kindle UI so that the device can be used normally.

当用户按下菜单按钮时，[stop.sh脚本](https://github.com/mariannefeng/kindle-hax/blob/main/kindle/custom-dash/bin/stop.sh)会自动被调用，它会终止仪表盘，清除屏幕，并重启Kindle UI，以便设备可以正常使用。

## Final Thoughts

## 最终想法

Now that it's been running for more than a month, 2 things I'm thinking about:

既然它已经运行了一个多月，我在考虑两件事：

### Color bleeding

### 颜色渗出

Even though I clear the screen twice before rendering a new image, the color bleed is still pretty noticeable after it's been running for a couple days. I have a theory that if I flash the screen completely black and then white again when the kindle goes to sleep at night, it'd solve the problem but haven't tried it out yet.

尽管我在渲染新图像之前清除屏幕两次，但在运行几天后，颜色渗出仍然相当明显。我有一个理论，如果我在Kindle晚上进入睡眠状态时让屏幕完全变黑然后变白，就能解决问题，但还没有尝试过。

### Battery life

### 电池续航

Right now it can go for ~5 days without being plugged in. I'd love for that number to be at the 2 week mark. Turning the device off for 10 hours at night extended the battery life by ~2 days, but 2 weeks is still a long ways off. I've debated increasing the gap between screen refreshes since it refreshes every minute right now, but I like the (almost) live minute updates so would rather sacrifice that last if possible in the quest for longer battery life.

现在它可以在不插电的情况下运行约5天。我希望这个数字能达到2周。晚上关闭设备10小时将电池续航延长了约2天，但2周还有很长的路要走。我在考虑增加屏幕刷新之间的间隔，因为它现在每分钟刷新一次，但我喜欢（几乎）实时的分钟更新，所以如果可能的话，我宁愿在追求更长电池续航时牺牲这一点。

Overall, this thing is sick! Probably one of the most fun projects I've built in recent memory. We use it every day before leaving the house, and it's *so* much simpler than texting a stop number to an NJ Transit phone number. I can see serving up all sorts of interesting information on the e-ink screen - calendar, weather, daily tasks, sky's the limit.

总的来说，这东西太酷了！可能是我最近记忆中最有趣的项目之一。我们每天出门前都用它，而且比给NJ Transit电话号码发短信查询站点要简单*得多*。我可以想象在电子墨水屏上显示各种有趣的信息——日历、天气、每日任务，天空才是极限。

---

## 批判性思考评论

这篇文章展示了一个非常有趣且实用的硬件改造项目，将废弃的Kindle电子阅读器转变为实时公交信息显示屏。以下是我的一些思考：

### 技术亮点

1. **资源利用的创新性**：作者将即将被淘汰的旧设备赋予了新的生命，这种"变废为宝"的思维方式值得提倡。在消费电子产品快速迭代的今天，这种改造项目具有环保意义。

2. **成本控制意识**：作者明确提到不想花140美元购买TRMNL，而是选择自己动手。这种DIY精神和对成本的关注是很多极客项目的驱动力。

3. **技术栈的务实选择**：当发现Puppeteer在廉价VPS上性能不佳时，作者灵活地改用wkhtmltoimage解决方案，展现了实际问题解决能力。

### 可改进之处

1. **电池续航的权衡**：作者提到目前5天的续航与理想的2周有差距。这反映了物联网设备中实时更新与电池寿命之间的经典权衡。也许可以考虑使用电子墨水屏的低功耗特性，采用"深度睡眠+定时唤醒"的策略。

2. **通用性问题**：该项目高度依赖NJ Transit的特定API，缺乏通用性。如果能设计一个更通用的框架，支持不同的数据源（天气、股票、日历等），项目的价值会更大。

3. **颜色渗出的技术局限**：电子墨水屏的固有特性导致了残影问题，这是当前技术的局限。作者提出的夜间全黑全白刷新方案理论上可行，但可能影响用户体验。

### 社会意义

这个项目体现了"智能家庭"的一个侧面——不一定是购买昂贵的商业化产品，而是利用现有资源创造个性化解决方案。它降低了智能家居的门槛，同时也培养了用户的技术能力和问题解决思维。

总的来说，这是一个优秀的个人项目，展示了技术爱好者如何将多个领域的知识（Linux系统管理、Web开发、硬件改装）整合起来解决实际问题。
