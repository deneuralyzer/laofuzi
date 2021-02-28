# 1.开启一个UDP端口侦听，开启TCP侦听
# 2.传入LasVegas消息后，开启TCP端口等待连接
# 3.传入LasVegas消息的，进行TCP连接
# 4.第一个连入的，确定游戏人数
# 5.开始游戏

import socket, threading, queue, LasVegasAssistant, time
import LasVegasTabletopInit, LasVegasPlayerOperations, LasVegasSettlement

class LV_Multiplayer:

    def bd(self, proto, port):
        proto.bind(('', port))

    def udprecv(self, udpproto, clients):
        while True:
            msg = udpproto.recvfrom(768)
            if msg[0].decode() == 'LasVegas':
                clients[msg[1][0]] = 0
                print(msg[1], msg[0])
                print(clients)

    def tcpaccept(self, tcpproto):
        # 有个弱智问题：输入的玩家数量低于已连接的玩家数量
        while True:
            clientsocket, clientinfo = tcpproto.accept()

            if clientinfo[0] in self.clientdict and len(self.clientdict) <= 6:

                self.clientdict[clientinfo[0]] = clientsocket
                self.clientlist.append((clientsocket, clientinfo))
                print(clientinfo, 'Accepted.')


                # 记录下来了玩家信息
                if len(self.clientdict) == 1:
                    self.tcpout(clientsocket, 'Total Players (Z, [1, 6]; 1 for remote hotseat):LVIN')
                    self.tcpin(clientsocket)
                    self.vipclient = clientsocket
                else:
                    self.tcpout(clientsocket, 'Accepted')
            else:
                self.tcpout(clientsocket, 'Full')


    def tcpout(self, client, text):
        client.send(text.encode())

    def tcpin(self, client):

        # 应该由客户端保证输入的为数字
        msg = client.recv(1024)
        msg = msg.decode('utf-8')
        print(msg)
        msg = ord(LasVegasAssistant.LV_Assistant.number_check(msg))

        msg = 6 if msg % 6 == 0 else msg % 6
        # 这个云单机我先鸽了
        if msg == 1:
            msg = 2
        self.player_number = msg

    def tcpbroadcast(self, clientlist, text):
        # clientlist就是self.clientlist，每个位置中记录了0：tcpsocket，1：clientinfo
        for item in clientlist:
            item[0].send(text.encode())

    def __init__(self):

        self.udpin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpin6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        trd1 = threading.Thread(target=self.bd, args=(self.udpin, 20211))
        trd1.start()
        self.clientdict = {} #-这两个其实是重复的但是我没想好怎么弄掉一个（咕咕咕）
        self.clientlist = [] #-
        self.vipclient = ''
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp6 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind(('', 20201))
        self.player_number = -1
        trd1.join()
        trd1 = threading.Thread(target=self.udprecv, args=(self.udpin, self.clientdict))
        trd1.start()
        self.tcp.listen(6)
        print(self.tcp)
        print('$$$')
        trd2 = threading.Thread(target=self.tcpaccept, args=(self.tcp,))
        trd2.start()

        # 运行到这的时候slef.player_number的值有-1，1，2，3，4，5，6几种
        # -1说明没人连进来或者没正确获得玩家数量，应当继续循环
        # 1说明选择了云人机模式，应当暂时排除，继续循环
        # 2-6都是可选的，如果实际连入人数多于选择的人数但不大于6，则以连入人数为准，结束循环
        # 如果连入人数与选择人数相等，则结束循环
        while True:
            if len(self.clientdict) == self.player_number:
                print('GJ')
                break
            elif len(self.clientdict) < self.player_number:
                time.sleep(1)
                print('Waiting for players...')
                print('Current Player(s): %d'%len(self.clientdict))
            elif self.player_number == -1:
                print('Waiting for player connecting.')
                time.sleep(5)
            elif len(self.clientdict) > self.player_number:
                self.player_number = len(self.clientdict)
                self.tcpout(self.vipclient, 'Idiot, %d players in total.'%self.player_number)
                print('Idiot VIP.')
                break
            elif self.player_number == 1:
                # 这是云单机，但我觉得不应该写在这个类里面，所以我就没写（咕咕咕
                pass
        # 给玩家发送位置消息
        time.sleep(5)
        for number in range(len(self.clientlist)):
            self.tcpout(self.clientlist[number][0], '你是玩家%d'%(number+1))
        print('Multiplayer Main')
        time.sleep(0.2)
        if self.player_number == 1:
            print('Remote Hotseat.')
            pass
        else:
            msgout = '共{0}个玩家'.format(self.player_number)
            self.tcpbroadcast(self.clientlist, msgout)
            time.sleep(0.2)
            self.tabletop = LasVegasTabletopInit.LV_Tabletop_Init(self.player_number)
            self.game_players = LasVegasPlayerOperations.LV_Player_Operations(self.player_number)
            self.current_player = 0
            self.gamble = 1
            while self.gamble <= 4:
                msgout = "赌局："+str(self.gamble) + '\n'
                print(msgout, end='')
                self.tcpbroadcast(self.clientlist, msgout)
                time.sleep(0.2)
                self.LV_game = 1
                if self.gamble > 1:
                    self.game_players.dice_refresh()
                    self.tabletop.casino_dices_renew(self.player_number)
                self.tabletop.casino_money_put()
                while self.LV_game <= 4:
                    # 第一轮
                    self.LV_round = 1
                    msgout = '第%d轮\n'%self.LV_game
                    print(msgout, end='')
                    self.tcpbroadcast(self.clientlist, msgout)
                    time.sleep(0.2)
                    while self.LV_round <= self.player_number:
                        # 控制投骰子的玩家的顺序
                        # 以3个玩家为例
                        # 投骰子顺序是：1，2，3，2，3，1，3，1，2，1，2，3
                        self.current_player = (self.gamble * 4) + self.LV_game + self.LV_round - 1 - 4
                        self.current_player = self.current_player % self.player_number
                        # 草，在单机模式里这里用的是dictionary，序号是从1开始的
                        # 也就是说使用self.clientlist的时候，currentplayer需要-1
                        if self.current_player == 0:
                            self.current_player = self.player_number
                        msgout = '玩家{0}投骰子\n'.format(self.current_player)
                        print(msgout, end='')
                        self.tcpbroadcast(self.clientlist, msgout)
                        time.sleep(0.2)
                        self.game_players.players[self.current_player]['dice'] = \
                            LasVegasAssistant.LV_Assistant.roll_dice_MP(
                                self.game_players.players[self.current_player]['dice'],
                                self.clientlist[self.current_player - 1][0])
                        msgout = LasVegasAssistant.LV_Assistant.show_casinos_MP(self.tabletop.casinos, self.player_number)
                        self.tcpbroadcast(self.clientlist, msgout)
                        time.sleep(0.2)
                        if self.game_players.players[self.current_player]['dice']['SP'] + sum(
                                self.game_players.players[self.current_player]['dice']['ND']) > -8:
                            # 显示骰子
                            msgout = LasVegasAssistant.LV_Assistant.show_dice_MP(
                                self.game_players.players[self.current_player]['dice'], self.current_player)
                            self.tcpbroadcast(self.clientlist, msgout)
                            time.sleep(0.2)
                            # 选骰子
                            self.selected_number = LasVegasAssistant.LV_Assistant.select_dice_MP(
                                self.game_players.players[self.current_player]['dice'],
                                self.clientlist[self.current_player - 1][0])
                            msgout = '选择了：{0}\n'.format(self.selected_number)
                            self.tcpbroadcast(self.clientlist, msgout)
                            time.sleep(0.2)
                            # 放骰子
                            diceremain = LasVegasPlayerOperations.LV_Player_Operations.put_dice(
                                self.game_players.players[self.current_player]['dice'],
                                self.selected_number,
                                self.tabletop.casinos[self.selected_number],
                                self.current_player)
                            msgout = '玩家{0}剩余{1}个骰子\n'.format(self.current_player, diceremain)
                            self.tcpbroadcast(self.clientlist, msgout)
                            time.sleep(0.2)
                            print(msgout)
                        self.LV_round += 1
                    self.LV_game += 1
                msgout = LasVegasSettlement.LV_Settlement.check_duplicate(self.tabletop.casinos, self.player_number)
                self.tcpbroadcast(self.clientlist, msgout)
                time.sleep(0.2)
                self.compared = LasVegasSettlement.LV_Settlement.comparison(self.tabletop.casinos, self.player_number)
                msgout = LasVegasSettlement.LV_Settlement.money_assignment(self.compared,
                                                                           self.tabletop.casinos,
                                                                           self.game_players.players,
                                                                           self.player_number)
                self.tcpbroadcast(self.clientlist, msgout)
                time.sleep(0.2)
                msgout = LasVegasAssistant.LV_Assistant.show_money(self.game_players.players)
                self.tcpbroadcast(self.clientlist, msgout)
                time.sleep(0.2)
                self.gamble += 1
            msgout = LasVegasAssistant.LV_Assistant.gamble_summary(self.game_players.players)
            self.tcpbroadcast(self.clientlist, msgout)
            time.sleep(0.2)
        for item in self.clientlist:
            item[0].close()


if __name__ == '__main__':
    T = LV_Multiplayer()