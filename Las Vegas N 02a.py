import random
import os

print("Las Vegas V 0.1a")
print("目前还不存在这样的一个版权声明")
# 给每个赌场放钱
def banknoteput(xa, xb):

    ya = 0
    yb = 0
    yc = 0
    for ya in range(0, 6):
        yb = 0

        '''金额小于5则继续放'''
        while sum(xa[ya]) < 5:
            yc = random.randint(1, 10)

            # 保证钞票数量足够
            while True:
                if xb[yc - 1] != 0:

                    # 钱数为0则放钱
                    if xa[ya][yb] == 0:
                        xa[ya][yb] = yc
                        yb += 1
                        xb[yc - 1] -= 1

                        break
                    else:
                        yb += 1

                else:
                    yc = random.randint(1, 10)
    return xa, xb


# 掷色子，xa为当前玩家的色子，xb为当前玩家的可用色子数量
def rolldice(xa, xb):
    for ya in range(xb):
        xa[ya] = random.randint(1, 6)

    return xa


# xa：currentplayer，xb：numberselect[]，xc：countj
def showresult(xa, xb, xc):
    print("玩家：", xa + 1, "选择了点数：", xb[xa], "，使用了", xc, "个骰子", "，置于赌场：", xb[xa])
    return


# 用于排序
def ta(xa):
    return xa[1]


# 用于假装有GUI

def drawgui(xa):
    print("*", end='')
    for ya in range(len(xa)):
        print("-", end='')
    print("*")
    print("|" + xa + "|")
    print("*", end='')
    for ya in range(len(xa)):
        print("-", end='')
    print("*")


'''第1局，第1场，第1轮'''
gamble = 0
turn = 0
Gameround = 0

'''2个玩家，playernum不能小于等于1'''
playernum = int(input("玩家数量（小于2人，大于6人为2，但现在输多少都是）"))
while True:
    if playernum < 2:
        playernum = 2

    elif playernum > 6:
        playernum = 2

    else:
        break

'''初始化每个玩家的骰子均为0'''
dice = [[0 for col in range(8)] for row in range(playernum)]
# print(dice)

# 初始化钞票总数
banknotenum = [10 for col in range(10)]
# print(banknotenum)

# 初始化六个赌场，每个赌场最多有5个钞票位
casino = [[0 for col in range(5)] for row in range(6)]
'''
Col↓|Row→   Casino0   1   2   3   4   5
0                   0   0   0   0   0   0  
1                   0   0   0   0   0   0
2                   0   0   0   0   0   0
3                   0   0   0   0   0   0
4                   0   0   0   0   0   0
'''

# 当前玩家为1号玩家(值为0)
currentplayer = 0

# 每个玩家所得钱数
playerbanknote = [0] * playernum

# 选择点数
numberselected = [0] * playernum

print("共", playernum, "个玩家。")
counti = 0
countj = 0
countk = 0

"""
for counti in range(0,6):

    countj = 0
    #金额小于5则继续放置
    while(sum(casino[counti]) < 5):

        countk = random.randint(1,10)

        #print("countk", countk)
        #print("countj",countj)


        while(True):
            #确定钞票数量足够
            if banknotenum[countk - 1] != 0:
                casino[counti][countj] = countk
                countj += 1
                banknotenum[countk - 1] -= 1
                #print(casino)
                break

            else:
                countk = random.randint(1,10)
                #print("elseA")

"""
# 军长AI
wangyueAI = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
# 按最大面值排序
def valuecasino(xa):
    ya = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    yb = xa
    for yc in range(6):

        for yd in range(6):
            if ya[yc][1] < yb[yd]:
                # 0位置储存赌场号，1位置储存最大钱数
                ya[yc][0] = yd
                ya[yc][1] = yb[yd]

        # 删掉钱数最多的赌场
        yb[ya[yc][0]] = 0
    
    return ya


# 赌局开始
for gamble in range(4):

    '''
    # 假装存在GUI
    # drawgui("gamble", gamble)

    '''
    
    '''
    print("*", end='')
    for counti in range(len("|gamble: " + str(gamble + 1)) + 1):
        print("-", end='')
    print("*")
    print("|Gamble:", gamble + 1, "|")
    print("*", end='')
    for counti in range(len("|gamble: " + str(gamble + 1)) + 1):
        print("-", end='')
    print("*")
    '''

    # 每个玩家可用骰子数量
    diceavail = [8 for col in range(playernum)]

    # 初始化每个人的置放情况
    dicestatue = [[0 for col in range(6)] for row in range(playernum)]
    '''
    列↓|行→  Casino0   1   2   3   4   5
    player0          0   0   0   0   0   0
    player1          0   0   0   0   0   0 
    ...
    '''
    # 每场开始
    for turn in range(4):

        # 假装存在GUI
        gameinfo = "Gamble:" + str(gamble + 1) + " Turn:" + str(turn + 1)
        drawgui(gameinfo)
        # print("turn:", turn)
        # 从大到小对钞票面值排序
        for counti in range(6):
            casino[counti].sort(reverse=True)
        # 每轮开始
        casino, banknotenum = banknoteput(casino, banknotenum)
        # 从大到小对钞票面值排序
        for counti in range(6):
            casino[counti].sort(reverse=True)

        # 对赌场最大面值排序
        tempa = [0, 0, 0, 0, 0, 0]
        for counti in range(6):
            tempa[counti] = casino[counti][0]
        # print(tempa)


        # 获得从大到小排列的每个赌场号及其最大的面值
        # 0：0-5的赌场号；1：面值
        wangyueAI = valuecasino(tempa)
        # print(wangyueAI)

        
        # 于此循环内，控制一轮投色子步骤
        for Gameround in range(playernum):

            # 前轮最先投色子的玩家，本轮最后投，前轮第二个投的玩家，本轮最先投，前轮第三个投的玩家，下轮最先投，以此循环
            currentplayer = (Gameround + turn) % playernum

            '''
            # 不可用骰子示数-1，可用骰子数减去示数为-1的骰子数量
            countj = 0
            for counti in dice[currentplayer]:
                if counti == -1:
                    countj += 1
            diceavail[currentplayer] = diceavail[currentplayer] - countj
            '''
            # 确定有没有色子
            if diceavail[currentplayer] != 0:
                # 掷色子
                dice[currentplayer] = rolldice(dice[currentplayer], diceavail[currentplayer])

                '''
                for countl in range(diceavail[currentplayer]):
                    print("currentplayer:", currentplayer)
                    print("countl:", countl, "range:", diceavail[currentplayer])
                    dice[currentplayer][countl] = random.randint(1, 6)
                '''

                for counti in range(6):
                    print("赌场", counti + 1, " ，金钱：", end = '')

                    for countj in range(5):

                        if casino[counti][countj] != 0:
                            print(casino[counti][countj], end = '')

                            if casino[counti][countj + 1] !=0:
                                print(" ,", end = '')

                            else:
                                print(" .")

                                break

                    # print("赌场", counti + 1, "金钱：", casino[counti])

                print("玩家", currentplayer + 1, "，掷得的点数：", dice[currentplayer])

                # AI制定策略

                # 军长AI
                # 确定掷得了什么点数（1-6的赌场号），排除不可用的-1
                WYa=[]
                for counti in dice[currentplayer]:
                    if (not counti in WYa) and (counti != -1):
                        WYa.append(counti)
                # print(WYa)

                # 确定都有几个色子
                WYb = [[0 for col in range(len(WYa))] for row in range(2)]
                WYc = 0
                for counti in WYa:
                    WYb[0][WYc] = counti
                    WYb[1][WYc] = dice[currentplayer].count(counti)
                    WYc += 1
                # 0：有什么色子（1-6的赌场号），1：有几个色子
                # print("#", WYb)
                
                # WYd：0位置记录可选的1-6赌场号，1位置记录赌场的最大面值，按照最大面值排序，然后按照赌场1-6顺序排序
                WYd = []
                countj = [0, 0]
                countk = 0
                for counti in range(6):
                    if (wangyueAI[counti][0] + 1) in WYa:
                        countj[0] = wangyueAI[counti][0] + 1
                        countj[1] = wangyueAI[counti][1]
                        # append:???
                        WYd.append([0,0])
                        
                        WYd[countk][0] = countj[0]
                        WYd[countk][1] = countj[1]
                        countk += 1
                    
                # print("$", WYd)

                # WYf记录钞票面值最大的几个赌场
                WYf = []
                for counti in range(len(WYa)):
                    if WYd[counti][1] == WYd[0][1]:
                        WYf.append(WYd[counti][0])
                # 给countk和countl赋初值，countk是WYf里第0位置的赌场的掷得的色子数量，countl记录色子数量最多的赌场号
                for counti in range(len(WYb[0])):
                    if WYf[0] == WYb[0][counti]:
                        countk = WYb[1][counti]
                        countl = WYf[0]
                        break

                # 如果还一样理当选已放置点数最多的，咕咕咕
                for counti in range(1, len(WYf)):
                    for countj in range(len(WYb[0])):
                        if countk + dicestatue[currentplayer][countl - 1] < dicestatue[currentplayer][WYb[0][countj] - 1] + WYb[1][countj]:
                            countk = WYb[1][countj]
                            countl = WYb[0][countj]


                '''
                
                # 看看可选的哪个赌场钱多，counk：最大面值从大到小排列的赌场号，面值相同时，按赌场序号从小到大排列
                countk = [0, 0, 0, 0, 0, 0]
                countl = 0
                for counti in range(6):
                    for countj in WYa:
                        if (countj - 1) == wangyueAI[counti][0]:
                            # 用WYa里的counj赋值，得到的是1-6的赌场号
                            countk[countl] = countj
                            countl += 1
                # countk需要保留一会儿
                print(countk)
                
                # 可选的两个最大面值赌场的最大面值钞票一样，需要看色子数量
                # countl 0位置记录可选的具有最大面值的赌场的赌场号(1-6)
                countl = [-1,-1]
                for counti in range(6):


                    for countj in range(len(WYa)):
                        # 找到掷得具有最大面值的赌场的赌场号(1-6)
                        if countk[counti] == WYa[countj]:
                            countl[0] = countk[counti]
                            break

                    if countl[0] != -1:
                        break

                # countl 1位置记录对应的可选的最大面值
                for counti in range(6):
                    if countl[0] == wangyueAI[counti][0] + 1:
                        countl[1] = wangyueAI[counti][1]
                        break
                '''
                    
                
                print("军长AI建议选择：", countl, "号赌场")

                

                # 选择点数
                numberselected[currentplayer] = int(input("选择一个点数："))
                while True:

                    if numberselected[currentplayer] != -1:

                        counti = 0
                        countj = 0

                        for counti in range(diceavail[currentplayer]):

                            if numberselected[currentplayer] == dice[currentplayer][counti]:

                                # 记录使用的骰子数量，用过的骰子点数记为-1
                                countj += 1
                                dice[currentplayer][counti] = -1

                        if countj != 0:

                            break

                        else:

                            numberselected[currentplayer] = int(input("错误的点数，选择一个新点数："))

                showresult(currentplayer, numberselected, countj)

                # 表示：dicestatue[玩家号][赌场号] = 玩家置放的色子数量
                dicestatue[currentplayer][numberselected[currentplayer] - 1] += countj
                '''
                print("玩家：", currentplayer + 1, "选择了点数：", numberselected[currentplayer], "，使用了", countj, "个骰子",
                      "，置于赌场：", numberselected[currentplayer])
                '''

                # 降序对骰子排序
                dice[currentplayer].sort(reverse = True)
                # 减少可用骰子数量
                diceavail[currentplayer] -= countj

            else:
                print("没有可用的色子。")

            print("玩家：", currentplayer + 1, "。所有骰子状态：", dice[currentplayer], "。剩余骰子数量：", diceavail[currentplayer])

            '''
            print(casino)
            print(banknotenum)
            
            print(dice)
            '''

            # 以下用于假装存在UI
            # print(dicestatue)

            print("\n*** G",gamble + 1 ," T", turn + 1, " R", Gameround + 1, " DICESTATUE ***")
            print("CASINO # ", end = '')
            for counti in range(6):
                print("|", counti + 1, "", end = '')

            print("")
            countk = "CASINO # | 1 | 2 | 3 | 4 | 5 | 6 "
            for counti in range(len(countk)):
                if countk[counti] == "|":
                    print("+", end = '')

                else:
                    print("-", end = '')

            print("")
            for counti in range(playernum):

                for countj in range(6):
                    if countj == 0:
                        print("PLAYER", counti + 1, "", end = '')

                    print("|", dicestatue[counti][countj], "", end = '')

                print("")
                    
            print("\n")

    '''一轮结束，结算'''
    # 查重
    countk = 0
    countl = 0
    countm = -1
    # 对每一个玩家
    for counti in range(playernum):

        # 对每一个赌场
        for countj in range(6):

            # 初始化
            countl = 0
            countm = -1
            # 若放置骰子数量不为0
            if dicestatue[counti][countj] != 0:
                # 记录骰子数量
                countl = dicestatue[counti][countj]
                # 记录玩家号
                countm = counti

                print("录得玩家", countm + 1, "在赌场", countj + 1, "有", countl, "个骰子")

                # 并对后续玩家进行检验
                for countk in range(counti + 1, playernum):

                    # 如果有相同点数
                    if dicestatue[countk][countj] == countl:

                        # 第一个玩家和相同点数玩家的点数均置零
                        dicestatue[counti][countj] = 0
                        dicestatue[countk][countj] = 0
                        print("测得玩家", countm + 1, "和", countk + 1, "在赌场", countj + 1, "有相同骰子数", countl)

    # print(dicestatue)

    # 开始结算
    # 记录所有玩家在0号赌场置放的骰子数量
    dicecomp = [[-1 for col in range(2)] for row in range(playernum)]

    '''
    列↓|行→   0   1
    player0     -1  -1
    player1     -1  -1
    ...
    '''
    # 0-5号赌场
    countj = 0
    for countj in range(6):

        for counti in range(playernum):
            # 0位置记录玩家号，1位置记录骰子数
            dicecomp[counti][0] = counti
            dicecomp[counti][1] = dicestatue[counti][countj]
            # print("loop", counti, "dicecomp in loop", dicecomp)
        '''
        E.g. #0赌场： 玩家0有2个骰子，玩家1有3个骰子，dicecomp看起来应该是：
        0   2
        1   3
        '''

        # 从置放骰子数量最多的玩家开始
        dicecomp.sort(key=ta, reverse=True)
        # print("dicecomp", dicecomp)

        countk = 0
        # counti：钞票位置
        for counti in range(playernum):
            # 如果置放的骰子数大于0
            if dicecomp[counti][1] > 0:
                # 如果countj号赌场上的countk位置还存有钞票
                if casino[countj][countk] != 0:
                    # 从第一个钞票位开始拿钱
                    playerbanknote[dicecomp[counti][0]] += casino[countj][countk]
                    casino[countj][countk] = 0
                    # 移动一个钞票位
                    countk += 1

    for counti in range(playernum):
        print("玩家：", counti + 1, "拥有金钱：", playerbanknote[counti])

counti = 0
countj = 0
countk = 0
for counti in range(playernum):
    if playerbanknote[counti] > countj:
        countj = playerbanknote[counti]
        countk = counti

    elif playerbanknote[counti] == 0:
        print("玩家", counti + 1, "是穷光蛋！")

print("玩家", countk + 1, "是孙子王！")
