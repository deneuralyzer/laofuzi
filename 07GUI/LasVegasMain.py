#
import LasVegasAssistant
# 单人模式
import LasVegasSingleMode

import LasVegasMultiPlayer
"""本部分包括游戏初始程序，包括模式选择，人数选择，以及可能的GUI等\n
LasVegasGameModeSelect.py并入本文件\n
LasVegasPlayerNumber.py并入本文件\n
新增LasVegasSingleMode.py文件"""

class LV_Game_Mode_Select:
    """模式选择模块，0为重选，1为单机，2为云单机，3为联机多人"""
    # 为什么不调用LasVegasAssisant呢？我就不
    check_number = lambda x: '1' if not x else x[0]

    def __init__(self):
        count = 0
        while True:
            print('选择游戏模式：\n1：单机\t2：云人机\t3：云多人')
            # 有个小问题，能不能调用LasVegasMain里的IPT呢，不能
            self.choice = input('-->')
            self.choice = LV_Game_Mode_Select.check_number(self.choice)
            self.choice = ord(self.choice)
            if self.choice % 4 == 1:
                self.choice = 1
                print('单机')
                break
            elif self.choice % 4 == 2:
                self.choice = 2
                print('云人机')
                break
            elif self.choice % 4 == 3:
                self.choice = 3
                print('云多人')
                break
            else:
                print('选择了光头，退出请按Y')
                self.choice = input('-->')
                self.choice = LV_Game_Mode_Select.check_number(self.choice)
                self.choice = ord(self.choice)
                if self.choice % 2 == 1:
                    self.choice = -1
                    break
                else:
                    count += 1
            if count == 9:
                print('你不对劲')
                self.choice = -1
                break

class LV_Player_Number_S:
    """本类为Las Vegas游戏的确定玩家数量模块（用于单机版的模块）\n
    没有输入时默认为2，输入不合规时依ASCii码确定具体人数，当输入合规时（2 - 6的整数）返回人数，\n
否则返回0，当接收到0时应弹出错误并结束游戏或询问是否下一局（没有做）\n
对传入的数据可不进行合规性检测，数据类型需要为字符串或数字，\
传入的数据格式为(数据，True)\n"""

    def __init__(self):
        """当输入内容为1时询问是否需要结束游戏，若结束游戏则玩家数量置为100，\
作为标识，在main里识别到100则结束游戏"""
        count = 0
        while True:

            self.selected_number = 0
            info = "确定玩家数量（最多6人）：\n-->"
            number = str(input(info))
            number = LasVegasAssistant.LV_Assistant.number_check(number)
            number = ord(number) % 6
            self.selected_number = 6 if number == 0 else 0 if number == 1 else number

            if self.selected_number == 0:
                print('玩家数量有误，需要退出吗（Y或N）：')
                temp = input('-->')
                temp = ord(LasVegasAssistant.LV_Assistant.number_check(temp))
                if temp % 2 == 1:
                    self.selected_number = 100
                    break
                else:
                    count += 1
            else:
                print('玩家数量：{0}'.format(self.selected_number))
                break
            if count > 9:
                print('你不对劲')
                break


# 以下正文
if __name__ == '__main__':
    print("***Las Vegas V07***")
    for i in range(3):
        print('请各位dalao批评指正')

    LasVegasAssistant.LV_Assistant.pigeon_coo('\n')
    game_mode = LV_Game_Mode_Select()

    if game_mode.choice == 1:
        player_number = LV_Player_Number_S().selected_number
        print(player_number)
        main_game = LasVegasSingleMode.Single_Mode_Game(player_number)
    elif game_mode.choice == 2:
        print('Unaccomplished')
    elif game_mode.choice == 3:
        print('Unaccomplished?')
        print('务必先确认本机的外网IP地址，将会使用20201作为TCP端口和20211作为UDP端口')
        main_game = LasVegasMultiPlayer.LV_Multiplayer()
    else:
        print('End')

