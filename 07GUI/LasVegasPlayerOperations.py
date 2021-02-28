class LV_Player_Operations:
    '''本类是否启用有待观察\n \
本类用于执行玩家的一些操作，但不包括选择骰子点数，这是为什么呢？'''

    def put_dice(x_dice, x_selected_number, x_target_casino, x_current_player, x_mode = 0):
        '''玩家放置骰子的步骤，此处直接调用了本类中self.players这个对象，\
传入的x_dice应当为self.players[current_player]，\
其形如{'SP': 1, 'ND':[1,1,1,1,1,1,-1]}；\
必须给定选择的点数x_selected_number，其类型为int；\
传入的x_target_casino应当为LasVegasTabletopInit.py文件中，\
LV_Tabletop_Init类中的self.casinos[x_selected_number]；\
本函数认为玩家有可用的骰子，若玩家没有可用的骰子，应在main中排除，\
即'SP'和'ND'中不全为-1，用过的骰子必须赋值-1；
传入的x_current_player应当为current_player，其类型为int；\
传入的x_mode用于表示大骰子模式，但是我们咕咕咕，咕咕咕'''
        y_remain = 0
        if x_mode == 0:
            if x_dice['SP'] == x_selected_number:
                x_dice['SP'] = -1
                x_target_casino['player' + str(x_current_player)] += 1
            for count in range(len(x_dice['ND'])):
                if x_dice['ND'][count] == x_selected_number:
                    x_dice['ND'][count] = -1
                    x_target_casino['player' + str(x_current_player)] += 1
            if x_dice['SP'] != -1:
                y_remain += 1
            for count in range(len(x_dice['ND'])):
                if x_dice['ND'][count] != -1:
                    y_remain += 1
        return y_remain
        pass

    def dice_refresh(self):
        for count in range(1, len(self.players) + 1):
            self.players[count]['dice']['SP'] = 1
            self.players[count]['dice']['ND'] = [1, 1, 1, 1, 1, 1, 1]

    def __init__(self, x_player_number):
        '''定义玩家拥有的骰子和钱数，骰子分为大骰子'SP'和一般骰子'ND'，\
这里面必须给定玩家数量x_player_number，其类型为int'''
        self.players = {}
        for count in range(x_player_number):
            self.players[count + 1] = {}
            player_dice = {
            'SP' : 1,
            'ND' : [1, 1, 1, 1, 1, 1, 1]
            }
            self.players[count + 1]['dice'] = player_dice
            del player_dice
            self.players[count + 1]['money'] = 0


