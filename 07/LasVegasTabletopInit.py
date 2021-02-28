import random

class LV_Tabletop_Init:
    """本类用于初始化桌面以及完成补足赌场上金额的步骤，本类好像还多了些不该有的\
东西，但是我咕咕咕，咕咕咕，咕咕咕"""
    
    def casino_money_sum(self):
        """直接调用了self.casinos"""
        for temp in self.casinos:
            self.casinos[temp]['total_notes'] = sum(self.casinos[temp]['banknotes'])

    def casino_money_put(self):
        """直接调用了self.casinos。\
如果钞票堆里没有钞票了那就不用放了"""
        for temp in self.casinos:
            # 钞票堆里没有钞票
            if sum(self.money_pile) == 0:
                break
            casino_banknote_location = 0
            while self.casinos[temp]['total_notes'] < 5:
                if sum(self.money_pile) == 0:
                    break
                if self.casinos[temp]['banknotes'][casino_banknote_location] == 0:
                    self.draw_banknote()
                    self.casinos[temp]['banknotes'][casino_banknote_location] = self.banknote_drawed
                    self.casino_money_sum()
                casino_banknote_location += 1

        # 这一段应该能给揉进去上面
        for temp in self.casinos:
            self.casinos[temp]['banknotes'].sort(reverse = True)

    def draw_banknote(self):
        """抽一张钞票看看，这里有一种情况是钞票都被取走了钞票堆里没有钞票，\
这种情况应当在抽钞票前排除"""
        while True:
            
            self.banknote_drawed = random.randint(1,10)
            if self.money_pile[self.banknote_drawed] > 0:
                self.money_pile[self.banknote_drawed] -= 1
                # print('draw_banknote ended')
                # print(self.money_pile)
                break

    def put_dice(self, x_dice, x_selected_number, x_casinos):
        pass

    def __init__(self, x_player_number):
        """传递的x_player_number参数不可少且必须为2~6之间的一个数字，\
这里不会检查这个数值是否正确"""
        # 1~10面值的钞票，每个面值有10张，这里让0位置置0省的越界
        self.money_pile = [10 for i in range(11)]
        self.money_pile[0] = 0
        # 这个部分↓应该放在别的类里对不对啊，不太对哦
        # 8个骰子，SP为大骰子，ND为小骰子
        # 这个变量没用了↓
        # player_dice = {
        #     'SP': 1,
        #     'ND': [1, 1, 1, 1, 1, 1, 1]
        #     }
        
        # single_casino = {'banknotes': [0,0,0,0,0], 'total_notes': 0}
        # 会共引这个↑对象，好像不行
        # 采用字典存储玩家的骰子和赌场的钞票的情况
        # self.players = {}
        player_name = []
        for i in range(x_player_number):
            player_name.append('player' + str(i+1))
            # self.players[i+1] = {}
            # self.players[i+1]['dice'] = {'SP':1, 'ND':[1,1,1,1,1,1,1]}
            # self.players[i+1]['money'] = 0
        player_name = tuple(player_name)

        # players的样子如下：
        # 1:{'dice': {'SP':1, 'ND':[1,1,1,1,1,1]}, 'money':0}
        # 1是数字，是玩家号，从1开始，dice是骰子点数，SP是大骰子，ND是一般骰子，
        # money是拥有钱数
        
        self.casinos = {}
        for i in range(1, 7):
            self.casinos[i] = {'banknotes': [0, 0, 0, 0, 0], 'total_notes': 0}
            for j in range(1, 1+x_player_number):
                self.casinos[i]['player'+str(j)] = 0
        
        # casinos的样子如下：
        # 1:{'banknotes': [0,0,0,0,0], 'total_notes':0, 'player1': 0, ...}
        # 1是数字，是赌场号，从1开始，banknotes记录所有钞票情况，
        # total_notes记录总价值，player1等等是玩家名，其值是放置的骰子数量


        wasted_test_codes = '''
        self.money_pile = [1 for i in range(11)]
        self.money_pile[0] = 0
        self.money_pile[10] = 0
        self.casino_money_put()
        print(self.casinos)
        self.casino_money_put()
        print("*",self.casinos)
        '''

    def casino_dices_renew(self, x_player_number):
        for i in range(1, 7):
            for j in range(1, 1+x_player_number):
                self.casinos[i]['player'+str(j)] = 0


# A = LV_Tabletop_Init(2)
