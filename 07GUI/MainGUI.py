import tkinter
import socket
import multiprocessing
import threading
import re
from tkinter import messagebox
import time
import queue


# 这里面的multiplayer只做客户端
class Application_Modeselect(tkinter.Frame):
    MODE = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.createWidget()


    def createWidget(self):
        self.btn1 = tkinter.Button(self.master, text='Single', command=self.start_single, state='disable')
        self.btn2 = tkinter.Button(self.master, text='Multiplayer', command=self.start_multiplayer)
        self.btn3 = tkinter.Button(self.master, text='Quit', command=self.quit_game)
        self.btn1.pack()
        self.btn2.pack()
        self.btn3.pack()

    def start_single(self):
        Application_Modeselect.MODE = 1
        self.master.destroy()

    def start_multiplayer(self):
        Application_Modeselect.MODE = 2
        self.master.destroy()


    def quit_game(self):
        self.master.destroy()


class Single_Main(tkinter.Frame):
    FONT = ('TimesNewRoman', 10)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.createWidget()

    def createWidget(self):
        pass


class Multiplayer_Config(tkinter.Frame):

    def __init__(self, master=None):
        super(Multiplayer_Config, self).__init__(master)
        self.CONFIG = {}
        self.line1 = []
        self.line2 = []
        self.line3 = []
        self.line4 = []
        self.IPv6_addr = tkinter.StringVar()
        self.IPv6_addr.set('')
        self.waring = tkinter.StringVar()
        self.waring.set('输错必玩不了')
        self.IPv4_addr = [tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar(), tkinter.IntVar()]
        self.IPv4_addr[0].set(192)
        self.IPv4_addr[1].set(168)
        self.IPv4_addr[2].set(1)
        self.port = [tkinter.IntVar(), tkinter.IntVar()]
        self.port[0].set(20211)
        self.port[1].set(20201)
        self.createWidget()

    def createWidget(self):
        self.line1.append(tkinter.Label(self.master, text='服务器IPv4地址：', width=20))
        self.line1[0].grid(column=0, row=0, columnspan=2)
        self.subframe1 = tkinter.Frame(self.master, width=20)
        self.line1.append(self.subframe1)
        self.line1[1].grid(column=2, row=0, columnspan=2)
        self.v4loc = []
        self.v4loc.append(tkinter.Entry(self.subframe1, textvariable=self.IPv4_addr[0], width=3))
        self.v4loc.append(tkinter.Label(self.subframe1, text='.'))
        self.v4loc.append(tkinter.Entry(self.subframe1, textvariable=self.IPv4_addr[1], width=3))
        self.v4loc.append(tkinter.Label(self.subframe1, text='.'))
        self.v4loc.append(tkinter.Entry(self.subframe1, textvariable=self.IPv4_addr[2], width=3))
        self.v4loc.append(tkinter.Label(self.subframe1, text='.'))
        self.v4loc.append(tkinter.Entry(self.subframe1, textvariable=self.IPv4_addr[3], width=3))
        for item in self.v4loc:
            item.pack(side='left')

        self.line2.append(tkinter.Label(self.master, text='服务器IPv6地址：', width=20))
        self.line2[0].grid(column=0, row=1, columnspan=2)
        self.line2.append(tkinter.Entry(self.master, textvariable=self.IPv6_addr, width=20, state='disable'))
        self.line2[1].grid(column=2, row=1, columnspan=2)
        self.line3.append(tkinter.Label(self.master, text='服务器端口号码：', width=20))
        self.line3[0].grid(column=0, row=2, columnspan=2)
        self.subframe2 = tkinter.Frame(self.master, width=20)
        self.line3.append(self.subframe2)
        self.line3[1].grid(column=2, row=2, columnspan=2)
        self.portloc = []
        self.portloc.append(tkinter.Label(self.subframe2, text='UDP:'))
        self.portloc.append(tkinter.Entry(self.subframe2, textvariable=self.port[0], width=5))
        self.portloc.append(tkinter.Label(self.subframe2, text='TCP:'))
        self.portloc.append(tkinter.Entry(self.subframe2, textvariable=self.port[1], width=5))
        for item in self.portloc:
            item.pack(side='left')

        self.line3[1].grid(column=2, row=2, columnspan=2)
        self.line4.append(tkinter.Label(self.master, textvariable=self.waring, width=10))
        self.line4[0].grid(column=0, row=3)
        self.line4.append(tkinter.Button(self.master, text='清空', width=10))
        self.line4[1].grid(column=1, row=3)
        self.line4.append(tkinter.Button(self.master, text='确认', command=self.confirm, width=10))
        self.line4[2].bind('<Enter>', self.configure_check_i)
        self.line4[2].bind('<Leave>', self.configure_check_o)
        self.line4[2].grid(column=2, row=3)
        self.line4.append(tkinter.Button(self.master, text='退出', command=self.quit_game, width=10))
        self.line4[3].grid(column=3, row=3)

    def quit_game(self):
        self.master.destroy()

    def confirm(self):
        self.CONFIG = {
            'UDP': self.port[0].get(),
            'TCP': self.port[1].get(),
        }
        if self.IPv6_addr.get():
            self.CONFIG['IPv6'] = self.IPv6_addr.get()
        else:
            v4 = ''
            for item in self.IPv4_addr:
                v4 += str(item.get())
                v4 += '.'
            v4 = v4[:-1]
            self.CONFIG['IPv4'] = v4

        self.master.destroy()

    def configure_check_i(self, event):
        try:
            if self.IPv6_addr.get():
                print('1')
                if self.port[0].get() <= 1024 or self.port[0].get() >= 65536:
                    self.line4[2]['state'] = 'disable'
                    self.waring.set('UDP端口错误')
                elif self.port[1].get() <= 1024 or self.port[1].get() >= 65536:
                    self.line4[2]['state'] = 'disable'
                    self.waring.set('TCP端口错误')
                else:
                    self.waring.set('v4,v6择一填写')
            else:
                for item in self.IPv4_addr:
                    item.get()
                if self.IPv4_addr[3].get() <= 0 or self.IPv4_addr[3].get() >= 255:
                    self.line4[2]['state'] = 'disable'
                    self.waring.set('IP地址错误')
                elif self.port[0].get() <= 1024 or self.port[0].get() >= 65536:
                    self.line4[2]['state'] = 'disable'
                    self.waring.set('UDP端口错误')
                elif self.port[1].get() <= 1024 or self.port[1].get() >= 65536:
                    self.line4[2]['state'] = 'disable'
                    self.waring.set('TCP端口错误')
                else:
                    self.waring.set('v4,v6择一填写')
        except:
            self.line4[2]['state'] = 'disable'
            self.waring.set('检查端口、IP')

    def configure_check_o(self, event):
        self.line4[2]['state'] = 'normal'


class Multiplayer_Connect(tkinter.Frame):
    INSTRUCTION_PLAYER_NUMBER = re.compile('LVIN$')

    def __init__(self, config, Q, tcp, tcp6, master=None):
        super().__init__(master)
        self.master = master
        self.config = config
        if 'IPv6' in self.config:
            self.udp = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            self.tcp = tcp6
        elif 'IPv4' in self.config:
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.tcp = tcp
        self.infomation = tkinter.StringVar()
        self.infomation.set('初始化')
        self.player_number = tkinter.IntVar()
        self.line1 = []
        self.line2 = []
        self.line3 = []
        self.line4 = []
        self.msgQ = Q
        self.connect_server()
        self.thread_control = True
        self.instruction_control = True
        self.recv_control = True
        self.createWidget()
        self.trd1 = threading.Thread(target=self.tcp_recv, args=(self.msgQ,))
        self.trd1.start()
        self.trd2 = threading.Thread(target=self.instructions, args=(self.msgQ,))
        self.trd2.start()


    def createWidget(self):
        self.line1.append(tkinter.Label(self.master, textvariable=self.infomation))
        self.line1[0].grid(column=0, row=0, columnspan=3)
        self.line2.append(tkinter.Radiobutton(self.master, text='1', value=1, variable=self.player_number))
        self.line2[0].grid(column=0, row=1)
        self.line2.append(tkinter.Radiobutton(self.master, text='2', value=2, variable=self.player_number))
        self.line2[1].grid(column=1, row=1)
        self.line2.append(tkinter.Radiobutton(self.master, text='3', value=3, variable=self.player_number))
        self.line2[2].grid(column=2, row=1)
        self.line3.append(tkinter.Radiobutton(self.master, text='4', value=4, variable=self.player_number))
        self.line3[0].grid(column=0, row=2)
        self.line3.append(tkinter.Radiobutton(self.master, text='5', value=5, variable=self.player_number))
        self.line3[1].grid(column=1, row=2)
        self.line3.append(tkinter.Radiobutton(self.master, text='6', value=6, variable=self.player_number))
        self.line3[2].grid(column=2, row=2)
        self.line4.append(tkinter.Button(self.master, text='提交', state='disable', command=self.confirm))
        self.line4[0].grid(column=0, row=3, columnspan=3)

    def connect_server(self):
        global THIRD_CONTROL
        try:
            if 'IPv6' in self.config:
                # print(self.config, 6)

                self.udp.sendto('LasVegas'.encode(), (self.config['IPv6'], self.config['UDP']))
                self.infomation.set('v6：发送UDP数据')

                self.infomation.set('v6：建立TCP通道')
                self.tcp.connect((self.config['IPv6'], self.config['TCP']))
            elif 'IPv4' in self.config:
                # print(self.config, 4)

                self.udp.sendto('LasVegas'.encode(), (self.config['IPv4'], self.config['UDP']))
                self.infomation.set('v4：发送UDP数据')

                self.infomation.set('v4：建立TCP通道')
                self.tcp.connect((self.config['IPv4'], self.config['TCP']))
            else:
                self.infomation.set('配置信息不正确')
                THIRD_CONTROL = False

        except:
            self.infomation.set('出现严重错误')
            THIRD_CONTROL = False
        self.infomation.set('TCP通道已建立')

    def tcp_recv(self, Q):
        global FIRST_CONTROL
        self.infomation.set('接收TCP信息')
        while FIRST_CONTROL:
            msg = self.tcp.recv(1024)
            msg = msg.decode()
            Q.put(msg)
            print(msg)
        if not FIRST_CONTROL:
            exit()

    def instructions(self, Q):
        global SECOND_CONTROL, FIRST_CONTROL, THIRD_CONTROL
        while SECOND_CONTROL:
            if Q.qsize() > 0:
                msg = Q.get()
                if msg == 'Accepted':
                    SECOND_CONTROL = False
                    FIRST_CONTROL = False
                    self.infomation.set('点提交，睿智tkinter')
                    self.line4[0]['state'] = 'normal'
                    # 就必须得让这个窗口运行出来
                    break
                elif msg == 'Full':
                    self.infomation.set('你来晚了，10秒后退出')
                    THIRD_CONTROL = False
                    FIRST_CONTROL = False
                    time.sleep(10)
                    SECOND_CONTROL = False
                    self.master.destroy()
                elif Multiplayer_Connect.INSTRUCTION_PLAYER_NUMBER.search(msg):
                    self.infomation.set('请确定玩家总数：')
                    self.line4[0]['state'] = 'normal'
                    SECOND_CONTROL = False
                    break
        if not SECOND_CONTROL:
            exit()

    def confirm(self):
        global FIRST_CONTROL
        if FIRST_CONTROL:
            self.tcp.send(str(self.player_number.get()).encode())
            self.infomation.set('玩家数量已提交')
        FIRST_CONTROL = False
        self.master.destroy()


class LV_MainGUI_MP(tkinter.Frame):

    def __init__(self, Q, tcp, serverIP, master=None):
        super().__init__(master)
        global FOURTH_CONTROL, FIFTH_CONTROL, LOCAL_IP
        self.msgQ = Q
        self.tcp = tcp
        self.default_font = ('TimesNewRoman', 10)
        self.total_player = 0
        self.counter_i = 0
        self.counter_j = 0
        self.yourself = 0
        self.line1 = []
        self.line1_text = [tkinter.StringVar() for i in range(7)]
        self.line1_text[0].set('多人游戏\n客户端')
        self.line1_text[1].set('第 轮')
        self.line1_text[2].set('第 局')
        self.line1_text[3].set('当前玩家：\n玩家 ')
        self.line1_text[4].set('本机IP：{0}（参考）\n服务器地址：{1}'.format(LOCAL_IP, serverIP))
        self.line1_text[5].set('系统信息')
        self.line1_text[6].set('聊天消息（未开放）')

        print('!')

        self.line2 = []
        self.line2_text = [tkinter.StringVar() for i in range(9)]
        self.line2_text[0].set('钞票')
        self.line2_text[1].set('赌场 #')
        self.line2_text[2].set('玩家：\n放置的色子数')
        self.line2_text[3].set('当前玩家标识')
        self.line2_text[4].set('玩家信息：')
        self.line2_text[5].set('拥有钱数')
        self.line2_text[6].set('剩余骰子')
        self.line2_text[7].set('系统信息')
        self.line2_text[8].set('聊天消息（未开放）')

        print('@')

        self.line3 = []
        self.line3_text = [tkinter.StringVar() for i in range(7)]
        self.line3_text[1].set('1')
        self.line3_text[4].set('玩家1')

        self.line4 = []
        self.line4_text = [tkinter.StringVar() for i in range(7)]
        self.line4_text[1].set('2')
        self.line4_text[4].set('玩家2')

        self.line5 = []
        self.line5_text = [tkinter.StringVar() for i in range(7)]
        self.line5_text[1].set('3')
        self.line5_text[4].set('玩家3')

        self.line6 = []
        self.line6_text = [tkinter.StringVar() for i in range(7)]
        self.line6_text[1].set('4')
        self.line6_text[4].set('玩家4')

        self.line7 = []
        self.line7_text = [tkinter.StringVar() for i in range(7)]
        self.line7_text[1].set('5')
        self.line7_text[4].set('玩家5')

        self.line8 = []
        self.line8_text = [tkinter.StringVar() for i in range(7)]
        self.line8_text[1].set('6')
        self.line8_text[4].set('玩家6')

        self.line9 = []
        self.line9_text = [tkinter.IntVar() for i in range(8)]
        self.line9_text.insert(0, tkinter.StringVar())
        self.line9_text[0].set('你的色子')

        self.line10 = []
        self.line10_text = [tkinter.StringVar()]
        self.line10_text[0].set('选择点数')
        self.selected_number = tkinter.IntVar()
        self.chat_message = tkinter.StringVar()

        self.line11 = []
        self.line11_text = ['投色子', '确认选择', '发消息', '垃圾游戏']
        self.name_tcp_recv = None
        self.name_instruction = None
        # if FOURTH_CONTROL:
        #     self.tcp_recv()
        # if FIFTH_CONTROL:
        #     self.instructions()
        self.trd3 = threading.Thread(target=self.tcp_recv)
        self.trd4 = threading.Thread(target=self.instructions)
        self.trd3.start()
        self.trd4.start()

        self.createWidget()


    def createWidget(self):
        # 1
        for self.counter_i in range(7):
            if self.counter_i < 4:
                self.line1.append(tkinter.Label(
                    self.master,
                    textvariable=self.line1_text[self.counter_i],
                    width=12,
                    height=3,
                    font=self.default_font,
                    borderwidth=1,
                    relief='solid'
                ))
            else:
                self.line1.append(tkinter.Label(
                    self.master,
                    textvariable=self.line1_text[self.counter_i],
                    width=36,
                    height=3,
                    font=self.default_font,
                    borderwidth=1,
                    relief='solid'
                ))

        # 2
        for self.counter_i in range(9):
            if self.counter_i < 7:
                self.line2.append(tkinter.Label(
                    self.master,
                    textvariable=self.line2_text[self.counter_i],
                    width=12,
                    height=2,
                    font=self.default_font,
                    borderwidth=1,
                    relief='solid'
                ))
            else:
                self.line2.append(tkinter.Label(
                    self.master,
                    textvariable=self.line2_text[self.counter_i],
                    width=36,
                    height=14,
                    font=self.default_font,
                    borderwidth=1,
                    relief='solid',
                    justify='left',
                    wraplength=260
                ))

        # L1 grid
        self.counter_i = 0
        self.counter_j = 0
        for self.counter_i in range(7):
            if self.counter_i < 4:
                self.line1[self.counter_i].grid(column=self.counter_i, row=0, sticky='NSEW')
                self.counter_j += 1
            else:
                self.line1[self.counter_i].grid(column=self.counter_j, row=0, columnspan=3, sticky='NSEW')
                self.counter_j += 3

        # L2 grid
        self.counter_j = 0
        for self.counter_i in range(9):
            if self.counter_i < 7:
                self.line2[self.counter_i].grid(column=self.counter_i, row=1, sticky='NSEW')
                self.counter_j += 1
            else:
                self.line2[self.counter_i].grid(column=self.counter_j, row=1, columnspan=3, rowspan=7, sticky='NSEW')
                self.counter_j += 3

        # L3-8
        self.auto_generate(7, self.line3, self.line3_text, 2)
        self.auto_generate(7, self.line4, self.line4_text, 3)
        self.auto_generate(7, self.line5, self.line5_text, 4)
        self.auto_generate(7, self.line6, self.line6_text, 5)
        self.auto_generate(7, self.line7, self.line7_text, 6)
        self.auto_generate(7, self.line8, self.line8_text, 7)

        # L9
        self.auto_generate(9, self.line9, self.line9_text, 8)

        # L10
        self.line10.append(tkinter.Label(
            self.master,
            textvariable=self.line10_text[0],
            width=12,
            height=1,
            font=self.default_font,
            borderwidth=1,
            relief='solid'
        ))
        for counter in range(6):
            self.line10.append(tkinter.Radiobutton(
                self.master,
                text=str(counter + 1),
                value=counter + 1,
                variable=self.selected_number,
                width=12,
                height=1,
                font=self.default_font,
                borderwidth=1,
                relief='solid',
                state='disable'
            ))
        for counter in range(7):
            self.line10[counter].grid(column=counter, row=9, sticky='NSEW')
        self.line10.append(tkinter.Entry(
            self.master,
            textvariable=self.chat_message,
            width=72,
            state='disable'
        ))
        self.line10[7].grid(column=7, row=9, columnspan=6, sticky='NSEW')

        # L11
        for counter in range(4):
            self.line11.append(tkinter.Button(
                self.master,
                text=self.line11_text[counter],
                font=self.default_font

            ))
        self.line11[0]['command'] = self.rolldice
        self.line11[1]['command'] = self.submit
        self.line11[1]['state'] = 'disable'
        self.line11[2]['command'] = self.send_message
        self.line11[3]['command'] = self.rubbish
        self.line11[0].grid(column=0, row=10, sticky='NSEW')
        self.line11[1].grid(column=1, row=10, sticky='NSEW')
        self.line11[2].grid(column=7, row=10, sticky='NSEW')
        self.line11[3].grid(column=8, row=10, sticky='NSEW')

        # print('+++')

    def rolldice(self):
        messagebox.showinfo(title='ROLL DICE', message='RESULT:0,0,0,0,0,0\nNOT AVAILABLE YET')

    def select_dice(self):
        messagebox.showinfo(title='SELECT DICE', message='NO AVAILABLE DICES')

    def send_message(self):
        msg = self.chat_message.get()
        self.line2_text[8].set(msg)
        messagebox.showinfo(title='MESSAGE', message='NOT AVAILABLE YET')

    def auto_generate(self, number, linelist, linetextlist, row):
        for counter in range(number):
            linelist.append(tkinter.Label(
                self.master,
                textvariable=linetextlist[counter],
                width=12,
                height=2,
                font=self.default_font,
                borderwidth=1,
                relief='solid'
            ))
        for counter in range(number):
            linelist[counter].grid(column=counter, row=row, sticky='NSEW')

    def rubbish(self):
        tkinter.messagebox.showinfo(title='COMPLAINT', message='LasVegas ver 0.7 gui\nby laofuzi')

    def instructions(self):
        global FIFTH_CONTROL, FOURTH_CONTROL
        CONDITION_TOTAL_PLAYER = re.compile('共(\d)个玩家', re.S)
        CONDITION_PLAYER = re.compile('你是玩家(\d)', re.S)
        CONDITION_GAMBLE = re.compile('赌局：(\d)', re.S)
        CONDITION_ROUND = re.compile('第(\d)轮', re.S)
        CONDITION_CURRENTPLAYER = re.compile('玩家(\d)投骰子', re.S)
        CONDITION_CASINO_INFO = re.compile('<(.*?)>', re.S)
        CONDITION_CASINO_NUMBER = re.compile('赌场#(\d)上的钞票情况是：', re.S)
        CONDITION_CASINO_NOTES = re.compile('LVD(\d{1,2})', re.S)
        CONDITION_CASINO_PLAYERDICES = re.compile('P(\d)放了DIC(\d)', re.S)
        CONDITION_NO_DICE = re.compile('没有可用的骰子', re.S)
        CONDITION_PLAYER_ROLL = re.compile('玩家(\d)掷得了', re.S)
        CONDITION_PLAYER_RESELECT = re.compile('可供选择的数字为：\n(.*?)$', re.S)
        CONDITION_PLAYER_BIG = re.compile('大骰子：(\d)B', re.S)
        CONDITION_PLAYER_SMALL = re.compile('(\d)s', re.S)
        CONDITION_NO_CHOICE = re.compile('你没得选', re.S)
        CONDITION_PLAYER_REMAIN = re.compile('玩家(\d)剩余(\d)个骰子', re.S)
        CONDITION_PLAYER_GAIN = re.compile('玩家(\d)有金钱(\d{1,3})货币单位；', re.S)
        CONDITION_GAME_END = re.compile('孙子王', re.S)
        # print(threading.currentThread().name)
        while FIFTH_CONTROL:
            if self.msgQ.qsize() > 0:
                # print('\n100')
                msg = self.msgQ.get()
                print(msg)
                self.line2_text[7].set(msg)
                player = CONDITION_PLAYER.match(msg)
                gamble = CONDITION_GAMBLE.match(msg)
                LV_round = CONDITION_ROUND.match(msg)
                currentplayer = CONDITION_CURRENTPLAYER.match(msg)
                casino_info = CONDITION_CASINO_INFO.findall(msg)
                no_dice = CONDITION_NO_DICE.search(msg)
                roll_player = CONDITION_PLAYER_ROLL.findall(msg)
                reselect = CONDITION_PLAYER_RESELECT.search(msg)
                no_choice = CONDITION_NO_CHOICE.findall(msg)
                player_remain = CONDITION_PLAYER_REMAIN.findall(msg)
                player_gain = CONDITION_PLAYER_GAIN.findall(msg)
                game_end = CONDITION_GAME_END.search(msg)
                if CONDITION_TOTAL_PLAYER.findall(msg):
                    self.total_player = int(CONDITION_TOTAL_PLAYER.findall(msg)[0])
                    continue
                elif player:
                    self.yourself = player.group()[-1]
                    self.line1_text[3].set('你是玩家{0}'.format(player.group()[-1]))
                    continue
                elif gamble:
                    self.line1_text[1].set(gamble.group())
                    # self.line3_text[6].set(8)
                    # self.line4_text[6].set(8)
                    if self.total_player <= 2:
                        self.line3_text[6].set(8)
                        self.line4_text[6].set(8)
                    if self.total_player <= 3:
                        self.line5_text[6].set(8)
                    if self.total_player <= 4:
                        self.line6_text[6].set(8)
                    if self.total_player <= 5:
                        self.line7_text[6].set(8)
                    if self.total_player <= 6:
                        self.line8_text[6].set(8)
                    continue
                elif LV_round:
                    self.line1_text[2].set(LV_round.group())
                    continue
                elif currentplayer:
                    currentplayer = str(currentplayer.group()[2])
                    if currentplayer == '1':
                        self.line3_text[3].set('-->')
                        self.line4_text[3].set('')
                        self.line5_text[3].set('')
                        self.line6_text[3].set('')
                        self.line7_text[3].set('')
                        self.line8_text[3].set('')
                    elif currentplayer == '2':
                        self.line3_text[3].set('')
                        self.line4_text[3].set('-->')
                        self.line5_text[3].set('')
                        self.line6_text[3].set('')
                        self.line7_text[3].set('')
                        self.line8_text[3].set('')
                    elif currentplayer == '3':
                        self.line3_text[3].set('')
                        self.line4_text[3].set('')
                        self.line5_text[3].set('-->')
                        self.line6_text[3].set('')
                        self.line7_text[3].set('')
                        self.line8_text[3].set('')
                    elif currentplayer == '4':
                        self.line3_text[3].set('')
                        self.line4_text[3].set('')
                        self.line5_text[3].set('')
                        self.line6_text[3].set('-->')
                        self.line7_text[3].set('')
                        self.line8_text[3].set('')
                    elif currentplayer == '5':
                        self.line3_text[3].set('')
                        self.line4_text[3].set('')
                        self.line5_text[3].set('')
                        self.line6_text[3].set('')
                        self.line7_text[3].set('-->')
                        self.line8_text[3].set('')
                    elif currentplayer == '6':
                        self.line3_text[3].set('')
                        self.line4_text[3].set('')
                        self.line5_text[3].set('')
                        self.line6_text[3].set('')
                        self.line7_text[3].set('')
                        self.line8_text[3].set('-->')
                    continue
                elif casino_info:
                    for item in casino_info:
                        casino_number = int(CONDITION_CASINO_NUMBER.findall(item)[0])
                        casino_money = CONDITION_CASINO_NOTES.findall(item)
                        casino_playerdices = CONDITION_CASINO_PLAYERDICES.findall(item)
                        if casino_number == 1:
                            self.line3_text[0].set('$' + ' $'.join(casino_money))
                            temptext = ''
                            counteri = 0
                            for temp in casino_playerdices:
                                temptext += 'P{0}:{1};'.format(temp[0], temp[1])
                                counteri += 1
                                if counteri == 3:
                                    temptext += '\n'
                            self.line3_text[2].set(temptext)
                            continue
                        if casino_number == 2:
                            self.line4_text[0].set('$' + ' $'.join(casino_money))
                            temptext = ''
                            counteri = 0
                            for temp in casino_playerdices:
                                temptext += 'P{0}:{1};'.format(temp[0], temp[1])
                                counteri += 1
                                if counteri == 3:
                                    temptext += '\n'
                            self.line4_text[2].set(temptext)
                            continue
                        if casino_number == 3:
                            self.line5_text[0].set('$' + ' $'.join(casino_money))
                            temptext = ''
                            counteri = 0
                            for temp in casino_playerdices:
                                temptext += 'P{0}:{1};'.format(temp[0], temp[1])
                                counteri += 1
                                if counteri == 3:
                                    temptext += '\n'
                            self.line5_text[2].set(temptext)
                            continue
                        if casino_number == 4:
                            self.line6_text[0].set('$' + ' $'.join(casino_money))
                            temptext = ''
                            counteri = 0
                            for temp in casino_playerdices:
                                temptext += 'P{0}:{1};'.format(temp[0], temp[1])
                                counteri += 1
                                if counteri == 3:
                                    temptext += '\n'
                            self.line6_text[2].set(temptext)
                            continue
                        if casino_number == 5:
                            self.line7_text[0].set('$' + ' $'.join(casino_money))
                            temptext = ''
                            counteri = 0
                            for temp in casino_playerdices:
                                temptext += 'P{0}:{1};'.format(temp[0], temp[1])
                                counteri += 1
                                if counteri == 3:
                                    temptext += '\n'
                            self.line7_text[2].set(temptext)
                            continue
                        if casino_number == 6:
                            self.line8_text[0].set('$' + ' $'.join(casino_money))
                            temptext = ''
                            counteri = 0
                            for temp in casino_playerdices:
                                temptext += 'P{0}:{1};'.format(temp[0], temp[1])
                                counteri += 1
                                if counteri == 3:
                                    temptext += '\n'
                            self.line8_text[2].set(temptext)
                            continue
                    continue
                elif no_dice or no_choice:
                    for counteri in range(1, 9):
                        self.line9_text[counteri].set(0)
                        if counteri < 7:
                            self.line10[counteri]['state'] = 'disable'
                    continue
                elif roll_player:
                    if str(roll_player[-1]) == str(self.yourself):
                        self.line11[1]['state'] = 'normal'
                        big_dice = CONDITION_PLAYER_BIG.findall(msg)
                        small_dice = CONDITION_PLAYER_SMALL.findall(msg)
                        if big_dice:
                            self.line9_text[1].set(int(big_dice[0]))
                            self.line10[int(big_dice[0])]['state'] = 'normal'
                            self.selected_number.set(int(big_dice[0]))
                        else:
                            self.line9_text[1].set(0)
                        if small_dice:
                            self.selected_number.set(int(small_dice[0]))
                            for counteri in range(2, 9):
                                if counteri-2 < len(small_dice):
                                    self.line9_text[counteri].set(int(small_dice[counteri-2]))
                                    self.line10[int(small_dice[counteri-2])]['state'] = 'normal'

                                else:
                                    self.line9_text[counteri].set(0)
                    continue
                # 改在上面了，下面这个应该触发不了
                elif reselect:
                    reselect = reselect[0].split(' ')

                    for item in reselect:
                        if item:
                            item = int(item)
                            self.line10[item]['state'] = 'normal'


                    continue
                elif player_remain:
                    player_No = int(player_remain[0][0])
                    player_dice = int(player_remain[0][1])
                    if player_No == 1:
                        self.line3_text[6].set(player_dice)
                    elif player_No == 2:
                        self.line4_text[6].set(player_dice)
                    elif player_No == 3:
                        self.line5_text[6].set(player_dice)
                    elif player_No == 4:
                        self.line6_text[6].set(player_dice)
                    elif player_No == 5:
                        self.line7_text[6].set(player_dice)
                    elif player_No == 6:
                        self.line8_text[6].set(player_dice)
                    # continue
                elif player_gain:
                    for item in player_gain:
                        player_No = int(item[0])
                        player_money = int(item[1])
                        if player_No == 1:
                            self.line3_text[5].set(player_money)
                        elif player_No == 2:
                            self.line4_text[5].set(player_money)
                        elif player_No == 3:
                            self.line5_text[5].set(player_money)
                        elif player_No == 4:
                            self.line6_text[5].set(player_money)
                        elif player_No == 5:
                            self.line7_text[5].set(player_money)
                        elif player_No == 6:
                            self.line8_text[5].set(player_money)
                    continue
                elif game_end:
                    FOURTH_CONTROL = False
                    FIFTH_CONTROL = False
                    # self.master.after_cancel(self.name_instruction)
                    # self.master.after_cancel(self.name_tcp_recv)
                    for item in self.line11:
                        item['state'] = 'disable'
                # if FIFTH_CONTROL:
                #     self.name_instruction = self.master.after(5, self.instructions)

    def submit(self):
        self.tcp.send(str(self.selected_number.get()).encode())
        self.line11[1]['state'] = 'disable'
        for number in range(1, 7):
            self.line10[number]['state'] = 'disable'

    def tcp_recv(self):
        global FOURTH_CONTROL
        while FOURTH_CONTROL:
            msg = self.tcp.recv(1024)
            msg = msg.decode()
            self.msgQ.put(msg)
            # if FOURTH_CONTROL:
            #     self.name_tcp_recv = self.master.after(5, self.tcp_recv)

# tkinter对多线程的支持是挺糟糕
FIRST_CONTROL = True  # 结束LV_connect的recv
SECOND_CONTROL = True  # 结束LV_connect的instruction
THIRD_CONTROL = True
FOURTH_CONTROL = True  # 结束MAIN_GUI_MP的recv
FIFTH_CONTROL = True  # 结束MAIN_GUI_MP的instruction

LOCAL_IP = socket.gethostbyname(socket.gethostname())
if __name__ == '__main__':

    modeselectGUI = tkinter.Tk()
    modeselectGUI.title('模式选择')
    modeselectGUI.geometry('200x200+100+100')
    ModeAPP = Application_Modeselect(modeselectGUI)
    modeselectGUI.mainloop()
    msgQueue = queue.Queue()
    tcpconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp6conn = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    if Application_Modeselect.MODE == 0:
        pass
    elif Application_Modeselect.MODE == 1:
        LV_root = tkinter.Tk()
        LV_root.title('拉斯维加斯0.7GUI 单人模式')
        LV_root.geometry('1000x500+100+100')
        LV_root.mainloop()
    elif Application_Modeselect.MODE == 2:
        LV_config = tkinter.Tk()
        LV_config.title('配置信息-多人模式')
        LV_config.geometry('350x100+100+100')
        configAPP = Multiplayer_Config(LV_config)
        LV_config.mainloop()
        if configAPP.CONFIG:
            LV_connect = tkinter.Tk()
            LV_connect.title('连接中-多人模式')
            LV_connect.geometry('60x110+100+100')
            connectAPP = Multiplayer_Connect(master=LV_connect, config=configAPP.CONFIG, Q=msgQueue, tcp=tcpconn, tcp6=tcp6conn)
            LV_connect.mainloop()

            # print('!')

            if THIRD_CONTROL:
                # print('?')
                server = configAPP.CONFIG['IPv4'] if configAPP.CONFIG['IPv4'] else configAPP.CONFIG['IPv6']
                LV_MP_root = tkinter.Tk()
                LV_MP_root.title('拉斯维加斯0.7GUI 客户端')
                LV_MP_root.geometry('1300x500+100+100')
                mainGUI = LV_MainGUI_MP(master=LV_MP_root, Q=msgQueue, tcp=tcpconn, serverIP=server)
                LV_MP_root.mainloop()
