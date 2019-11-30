# Danmucraft（弹幕争霸）——我的世界 bilibili 直播间互动插件

Danmucraft（弹幕争霸）是基于 [blivedm](https://github.com/xfgryujk/blivedm) 开发的一个 bilibili 直播间插件。观众可以通过投喂金瓜子或银瓜子礼物获得点数，并消耗点数向主播所在的 Minecraft 世界发送命令。现版本可使用的命令如下：

# 命令

## 召唤 怪物名称
发送【召唤 苦力怕】，可在主播当前位置生成一只苦力怕。所有支持的实体名称，请参阅 [Minecraft_Wiki:译名标准化 - 实体](https://minecraft-zh.gamepedia.com/index.php?title=Minecraft_Wiki:%E8%AF%91%E5%90%8D%E6%A0%87%E5%87%86%E5%8C%96&variant=zh#.E5.AE.9E.E4.BD.93)。
P.S. 现已支持【召唤 闪电苦力怕】的命令。

怪物被分为四个不同的层级：
* 中立怪物（如：鸡）——几乎没有威胁，消耗 1000 点数；
* 敌对怪物（如：苦力怕）——威胁度较小，消耗 2000 点数；
* 精英怪物（如：唤魔者）——威胁度较高，消耗 10000 点数；
* Boss怪物（如：凋灵）——威胁度极高，召唤一次需消耗大量点数，但可群体召唤（见下）。

【召唤 TNT】已经被禁止使用。

## 召唤 Boss名称 (想投入点数)
召唤 Boss怪物的流程与召唤普通怪物有所不同。Minecraft 中的三个 Boss——末影龙、凋灵、远古守卫者都有其各自的召唤池，观众可发送弹幕【召唤 凋灵】将 5000 点数投入召唤池中（若可用点数 <5000 则全部投入），或者发送【召唤 凋灵 20000】将任意数额的点数投入召唤池中。
一旦 Boss 召唤池中的点数大于其消耗，将立即在主播的 Minecraft 世界中召唤相应 Boss，召唤池也将重置。

## 送 物品名称 (可选数量)
发送【送 钻石剑 4】命令可将四把钻石剑放入主播的背包栏中。不指定数量则默认为 1；数量最大为 16。
除了【附魔金苹果】每个消耗 500 点数以外，每件物品消耗 100 点数。
所有支持的物品名称，请参阅 [Minecraft_Wiki:译名标准化 - 方块](https://minecraft-zh.gamepedia.com/index.php?title=Minecraft_Wiki:%E8%AF%91%E5%90%8D%E6%A0%87%E5%87%86%E5%8C%96&variant=zh#.E6.96.B9.E5.9D.97) 和 [Minecraft_Wiki:译名标准化 - 物品](https://minecraft-zh.gamepedia.com/index.php?title=Minecraft_Wiki:%E8%AF%91%E5%90%8D%E6%A0%87%E5%87%86%E5%8C%96&variant=zh#.E7.89.A9.E5.93.81)。

## 拿 物品名称 (可选数量)
发送【拿 附魔金苹果 2】命令可从主播的背包栏中拿走两个附魔金苹果（没有则不会生效）。不指定数量则默认为 1；数量最大为 4。

拿走物品的消耗将是给予物品消耗的 10 倍；

## 效果 效果名称
发送【效果 速度】命令可赋予主播相应的效果。Buff（如：抗性提升） 持续时间默认为 180 秒；Debuff（如：失明） 持续时间则为 10 秒到 30 秒不等。

除【中毒】【凋零】两个稳定伤害效果消耗 10000 点数外，其余所有效果均消耗 3000 点数。

【瞬间伤害】效果已被禁止使用。

所有支持的效果名称，请参阅 [Minecraft_Wiki:译名标准化 - 状态效果](https://minecraft-zh.gamepedia.com/index.php?title=Minecraft_Wiki:%E8%AF%91%E5%90%8D%E6%A0%87%E5%87%86%E5%8C%96&variant=zh#.E7.8A.B6.E6.80.81.E6.95.88.E6.9E.9C) 。

## 清除 效果名称
发送【清除 速度】命令可清除主播相应的效果。所有效果清除都是立刻生效，不管该效果的剩余时间还有多长。

清除效果的消耗将是赋予效果消耗的 2 倍；

## 设置时间 时间名
发送【设置时间 早上】可立刻将主播世界的时间设定为早上。可选的时间包括：
【早上】【中午】【黄昏】【晚上】【夜晚】【傍晚】【午夜】【凌晨】【日出】【黎明】

每条命令消耗 2000 点数。

# 点数获取

观众通过投喂金瓜子或银瓜子礼物来获取直播间的点数，兑率如下：
* 100 银瓜子礼物 = 100 积分
* 100 金瓜子礼物 = 500 积分

开通舰长、总督不加任何积分。

不同日期的开播，积分不累加。

# 插件的安装及使用

为了使用 Danmucraft 插件，你必须：
* 会开设自己的 Minecraft 服务器（在命令行中运行）
* 安装 Python 3

## 服务器端的配置
关于如何架设自己的 Minecraft 服务器，请参阅 [Minecraft_Wiki:教程/架设服务器](https://minecraft-zh.gamepedia.com/index.php?title=%E6%95%99%E7%A8%8B/%E6%9E%B6%E8%AE%BE%E6%9C%8D%E5%8A%A1%E5%99%A8&variant=zh)

你的 Minecraft 服务器必须运行在名为 server 的 screen session 中，具体操作方式为：
* `$ screen -S server`
* `$ java -Xms1024M -Xmx2048M -jar minecraft_server.jar nogui`

待 Minecraft 服务器在 screen 内顺利运行后，服务器端的设置就算完成，现在你应该能进入到自己刚开设的 Minecraft 服务器中。

## Python 脚本的配置
首先使用 `pip install asyncio` 安装运行所需的库。随后用文本编辑器打开 `danmucraft.py`，必须修改的参数如下：
* `room_id`：直播间房号；
* `private_key`：使用 `ssh` 远程登录服务器所需的私钥存放地址；
* `server_address`：格式为 `username@server_ip_address`，用于登录到服务器。

可选修改的参数如下：
* `scale`：瓜子兑点数的倍率；
* `clear_item_scale`：清除物品之于给予物品的点数倍率；
* `clear_effect_scale`：清除效果之于赋予效果的点数倍率；
* `bosses_list`：初始化 Boss 列表，方便继承上次直播的数据。

配置完成后，使用 `python danmucrafy.py` 运行该脚本。
在运行过程中，`bosses.txt` 和 `log.txt` 两个文件会实时更新，可将文本中的信息展示在 OBS 中提高互动效果。

## 命令及消耗点数的配置
`dictionary.txt` 文件中包含了所有可召唤/给予的怪物/物品，其基本格式为：
实体/物品名 英文名 点数 (额外参数)
只有 `dictionary.txt` 存在的怪物/物品才可以被弹幕命令调用。若想要禁止某个物品被调用，可以使用 `# ` 将对应的行注释掉。
要修改某个怪物/物品的消耗点数，修改文件中对应的行即可。

# 关于 Probe
一个什么内容（游戏、音乐、直播）都做的创作者：
* [Bilibili 主页](https://space.bilibili.com/488744)
* [Bilibili 直播间](https://live.bilibili.com/16670)
* [Youtube 频道](https://www.youtube.com/channel/UCb-z8x0TD6cPtGkFLlUi4Sw)
* [网易云音乐](https://music.163.com/user/home?id=50587279)

欢迎大家关注 \_(:з」∠)\_
