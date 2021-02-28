# 该文件是没什么卵用但也导入省得在main里定义函数部分
from LasVegasAssistant import *
# 该文件是桌面初始化和摸钱部分
from LasVegasTabletopInit import *
# 该文件是摇摇乐或者摇摇不乐部分
from LasVegasPlayerOperations import *
# 该文件决定了谁是孙子王
from LasVegasSettlement import *


class Single_Mode_Game:
    """单人模式"""
    # 确定单机玩家数量
    def __init__(self, x_player_number):
        self.player_number = x_player_number

        self.tabletop = LV_Tabletop_Init(self.player_number)

        self.game_players = LV_Player_Operations(self.player_number)
        self.current_player = 0
        # 这里好像缺个循环
        self.gamble = 1
        while self.gamble <= 4:
            print('赌局：', self.gamble)
            self.LV_game = 1
            if self.gamble > 1:
                self.game_players.dice_refresh()
                self.tabletop.casino_dices_renew(self.player_number)
            self.tabletop.casino_money_put()

            while self.LV_game <= 4:
                # 第一轮
                self.LV_round = 1
                print('第{0}轮'.format(self.LV_game))

                while self.LV_round <= self.player_number:
                    # 控制投骰子的玩家的顺序
                    # 以3个玩家为例
                    # 投骰子顺序是：1，2，3，2，3，1，3，1，2，1，2，3
                    self.current_player = (self.gamble * 4) + self.LV_game + self.LV_round - 1 - 4
                    self.current_player = self.current_player % self.player_number
                    if self.current_player == 0:
                        self.current_player = self.player_number

                    # 开始投骰子
                    print('玩家{0}投骰子'.format(self.current_player))

                    self.game_players.players[self.current_player]['dice'] = LV_Assistant.roll_dice(
                        self.game_players.players[self.current_player]['dice'])
                    # 显示场上情况
                    LV_Assistant.show_casinos(self.tabletop.casinos, self.player_number)
                    # 以下用来输出投出的骰子情况
                    # 这里要求用过的骰子必须标记为-1
                    if self.game_players.players[self.current_player]['dice']['SP'] + sum(
                            self.game_players.players[self.current_player]['dice']['ND']) > -8:
                        # 显示骰子
                        LV_Assistant.show_dice(self.game_players.players[self.current_player]['dice'], self.current_player)
                        # 选骰子
                        self.selected_number = LV_Assistant.select_dice(self.game_players.players[self.current_player]['dice'])
                        # 放骰子
                        LV_Player_Operations.put_dice(self.game_players.players[self.current_player]['dice'], self.selected_number,
                                                      self.tabletop.casinos[self.selected_number], self.current_player)
                    # print(tabletop.casinos)

                    self.LV_round += 1

                self.LV_game += 1
            LV_Settlement.check_duplicate(self.tabletop.casinos, self.player_number)
            self.compared = LV_Settlement.comparison(self.tabletop.casinos, self.player_number)
            LV_Settlement.money_assignment(self.compared, self.tabletop.casinos, self.game_players.players, self.player_number)
            # print(game_players.players)
            LV_Assistant.show_money(self.game_players.players)
            self.gamble += 1
        LV_Assistant.gamble_summary(self.game_players.players)

