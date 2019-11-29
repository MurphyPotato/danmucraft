# -*- coding: utf-8 -*-
import os
import asyncio
import blivedm

# 在这里填入房间号
room_id = 16670

# 需要用到的命令，请根据自己的服务器情况修改
ssh_screen = "ssh -i ~/.ssh/minecraft minecraft@34.82.0.93 'screen -S server -p 0 -X stuff "
quote_left = '"'
quote_right = '''^M"'
'''

# Boss 列表
boss_list = ["elder_guardian", "ender_dragon", "wither"]

# 精英列表
elite_list = ["evoker", "ghast", "giant",
              "guardian", "illusioner", "ravager", "shulker", "end_crystal", "witch", "wither_skeleton", "phantom", "skeleton_horseman", "vindicator"]

# 怪物列表
enemy_list = ["blaze", "cave_spider", "chicken_jockey",
              "creeper", "drowned", "enderman", "endermite", "husk", "illager", "illager_captain", "iron_golem", "killer_bunny", "killer_rabbit", "magma_cube", "pigman", "pillager", "silverfish", "skeleton", "slime", "snow_golem", "spider", "spider_jockey", "stray", "vex", "zombie", "zombie_pigman", "zombie_villager"]


class Commands():
    def __init__(self, english, cost, param):
        self.english = english
        self.cost = int(cost)
        self.param = param


class Audience():
    def __init__(self, name, credit):
        self.name = name
        self.credit = 0

    def addSilver(self, coin):
        self.credit += coin * scale

    def addGold(self, coin):
        self.credit += coin * 5 * scale

    def subtractCredit(self, coin):
        self.credit -= coin
        self.printCost(coin)

    def printCredit(self):
        Log(f'{self.name} 当前 Credit: {self.credit}')

    def printCost(self, cost):
        Log(f'{self.name} 消耗: {cost}')


class Bosses():
    def __init__(self, name, credit):
        self.name = name
        self.credit = credit
        if self.name == "ender_dragon":
            self.cost = 600000
        if self.name == "wither":
            self.cost = 250000
        if self.name == "elder_guardian":
            self.cost = 100000

    def addCredit(self, credit):
        self.credit += credit

    def resetCredit(self):
        self.credit = self.credit - self.cost

    def isSummonable(self):
        return self.credit >= self.cost

    def printToFile(self, file):
        if self.name == "ender_dragon":
            file.write(f"末影龙： {self.credit}/{self.cost}\n")
        if self.name == "wither":
            file.write(f"凋灵： {self.credit}/{self.cost}\n")
        if self.name == "elder_guardian":
            file.write(f"远古守护者： {self.credit}/{self.cost}\n")


def getDictionary():
    d = {}
    with open('dictionary.txt') as f:
        lines = f.readlines()
    for line in lines:
        if(line[0] != "#"):
            word = line.split()
            if len(word) < 4:
                chinese, english, cost = word[0], word[1], word[2]
                d[chinese] = Commands(english, int(cost), '')
            elif len(word) >= 4:
                chinese, english, cost, param = word[0], word[1], word[2], word[3]
                d[chinese] = Commands(english, int(cost), param)
    return d


def Log(info):
    print(info)
    with open('log.txt', 'a') as file:
        file.write(info)
        file.write('\n')
    return


def sendCommand(mc_command):
    Log(f"已发送命令： {mc_command}")
    command = ssh_screen + quote_left + mc_command + quote_right
    os.system(command)
    return command


def checkDanmu(danmu):
    """
    code:
        -1 default / no action
        0 summon mob
        1 summon boss / add credit to the boss pool
        2 give item
        3 clear one item
        4 effect give
        5 effect clear
        6 set time
    """
    code = -1
    cost = 0
    payment = 5000
    num = 1
    string = "nothing"
    param = ''
    length = len(danmu.split())
    if(("召唤 " in danmu)):
        danmaku = danmu.split()[1]
        string, cost, param = parseDanmu(danmaku)
        if string != "nothing":
            if string not in boss_list:
                code = 0
            else:
                code = 1
        if(length > 2):
            payment = int(danmu.split()[2])
        return [code, string, cost, param, payment]

    elif(("送 " in danmu or "给 " in danmu)):
        if(length > 2):
            num = int(danmu.split()[2])
            if(num >= 16):
                num = 16
        else:
            num = 1
        danmaku = danmu.split()[1]
        string, cost, param = parseDanmu(danmaku)
        if string != "nothing":
            code = 2
        return [code, string, cost, param, num]

    elif(("拿 " in danmu or "拿走 " in danmu)):
        if(length > 2):
            num = int(danmu.split()[2])
            if(num >= 16):
                num = 8
        else:
            num = 1
        danmaku = danmu.split()[1]
        string, cost, param = parseDanmu(danmaku)
        if string != "nothing":
            code = 3
        return [code, string, cost, param, num]

    elif(("效果 " in danmu or "赋予 " in danmu)):
        danmaku = danmu.split()[1]
        string, cost, param = parseDanmu(danmaku)
        if string != "nothing":
            code = 4
        return [code, string, cost, param, num]

    elif(("清除效果 " in danmu or "清除 " in danmu)):
        danmaku = danmu.split()[1]
        string, cost, param = parseDanmu(danmaku)
        if string != "nothing":
            code = 5
        return [code, string, cost, param, num]

    elif(("设置时间 " in danmu)):
        danmaku = danmu.split()[1]
        string, cost, param = parseDanmu(danmaku)
        if string != "nothing":
            code = 6
        return [code, string, cost, param, num]

    return [code, string, cost, param, num]


def parseDanmu(danmu):
    if danmu in d.keys():
        string = d[danmu].english
        cost = d[danmu].cost
        param = d[danmu].param
    else:
        string = 'nothing'
        cost = 0
        param = ''
    return [string, cost, param]


def goSummon(string, param=''):
    if param != '':
        command = f"execute at @r run summon {string} ~ ~ ~ {param}"
    else:
        command = f"execute at @r run summon {string} ~ ~ ~"
    return command


def goGive(string, num):
    command = f"give @r {string} {num}"
    return command


def goClear(string, num):
    command = f"clear @r {string} {num}"
    return command


def goEffectGive(string, param):
    if param != '':
        command = f"effect give @a {string} {param}"
    else:
        command = f"effect give @a {string}"
    return command


def goEffectClear(string):
    command = f"effect clear @a {string}"
    return command


def goSetTime(string):
    command = f"time set {string}"
    return command


def updateBosses():
    with open('bosses.txt', 'w') as f:
        for boss in bosses_list:
            boss.printToFile(f)


# 中英文对照表
d = getDictionary()

# 获得点数的比例（一般为 1）
scale = 1

# 观众列表，观众投喂礼物后获得积分并进入此列表
audience_list = []
name_list = []

# 初始化 boss 列表，方便继承上次直播的数据
bosses_list = [Bosses("ender_dragon", 528900), Bosses(
    "wither", 8300), Bosses("elder_guardian", 400)]


class MyBLiveClient(blivedm.BLiveClient):
    # 演示如何自定义handler
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def __on_vip_enter(self, command):
        Log(command)
    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter  # 老爷入场

    async def _on_receive_popularity(self, popularity: int):
        print(f'当前人气值：{popularity}')

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        Log(f'{danmaku.uname}：{danmaku.msg}')
        if (danmaku.uname in name_list):
            index = name_list.index(danmaku.uname)
            thisguy = audience_list[index]
            code, string, cost, param, num = checkDanmu(danmaku.msg)
            total_cost, command = 0, ''
            payment = 0
            if code != -1:
                if code == 0:
                    # summon mob
                    total_cost = cost
                    command = goSummon(string, param)
                elif code == 1:
                    # summon boss
                    for boss in bosses_list:
                        if string == boss.name:
                            thisboss = boss
                            break
                    total_cost = cost
                    payment = num
                    command = goSummon(string, param)
                elif code == 2:
                    # give item
                    total_cost = cost*num
                    command = goGive(string, num)
                elif code == 3:
                    # clear item
                    total_cost = cost*num*5
                    command = goClear(string, num)
                elif code == 4:
                    # give effect
                    total_cost = cost
                    command = goEffectGive(string, param)
                elif code == 5:
                    # clear effect
                    total_cost = cost*2
                    command = goEffectClear(string)
                elif code == 6:
                    # set time
                    cost = 2000
                    command = goSetTime(string)

            if code == 1:
                # summon boss
                if (thisguy.credit >= total_cost):
                    pass
                elif (thisguy.credit < total_cost and thisguy.credit > payment):
                    cost = payment
                elif (thisguy.credit < payment):
                    cost = thisguy.credit
                thisguy.subtractCredit(cost)
                thisguy.printCredit()
                thisboss.addCredit(cost)
                if(thisboss.isSummonable()):
                    thisboss.resetCredit()
                    sendCommand(command)
                    Log(f"已召唤 {thisboss.name}")
                else:
                    Log(
                        f"{thisboss.name} 的当前召唤进度：{thisboss.credit}/{thisboss.cost}")
                updateBosses()

            elif (thisguy.credit >= total_cost):
                if code == -1:
                    pass
                elif code == 0 or code == 2 or code == 3 or code == 4 or code == 5 or code == 6:
                    # summon mod / give item / clear item / give effect / clear effect / reset time /
                    thisguy.subtractCredit(total_cost)
                    thisguy.printCredit()
                    sendCommand(command)
            else:
                Log(f"{{thisboss.name}} 的积分暂且不足~")
                thisguy.printCredit()
        else:
            Log("抱歉~尚未取得任何积分~")

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        # coin_type: silver/gold
        if(gift.uname not in name_list):
            name_list.append(gift.uname)
            audience_list.append(Audience(gift.uname, 0))
        if(gift.uname in name_list):
            index = name_list.index(gift.uname)
            thisguy = audience_list[index]
            coin = int(gift.total_coin)
            if(gift.coin_type[0] is 's'):
                thisguy.addSilver(coin)
            elif(gift.coin_type[0] is 'g'):
                thisguy.addGold(coin)
        Log(f'{gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')
        thisguy.printCredit()

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        Log(f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        Log(f'醒目留言 ¥{message.price} {message.uname}：{message.message}')


async def main():
    # Probe: 16670
    # Hyde: 3606383
    # 如果SSL验证失败就把ssl设为False
    client = MyBLiveClient(room_id, ssl=True)
    future = client.start()
    try:
        # 5秒后停止，测试用
        # await asyncio.sleep(5)
        # future = client.stop()
        # 或者
        # future.cancel()

        await future
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
