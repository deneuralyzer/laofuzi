import random
import socket


class LV_Assistant:
    """用来定义一些有什么卵用但是又不想写在main文件里的函数，这个类不应该被实例化\
    \n也就说这个类是个工具人"""

    def number_check(x_in, x_default='0'):
        """检定数字"""
        result = x_default if not x_in else x_in
        result = str(result)
        return result[0]

    def roll_dice(x_player_dice):
        """用来掷骰子，传入的x_player_dice应该为特定玩家的仅含{'SP': ?, 'ND': [?,?,?,?,?,?,?]}的字典，
        这里要求用过的骰子必须赋值-1"""
        if x_player_dice['SP'] + sum(x_player_dice['ND']) < -7:
            print('但你没有可用的骰子')
            return x_player_dice
        if x_player_dice['SP'] != -1:
            x_player_dice['SP'] = random.randint(1, 6)
        if sum(x_player_dice['ND']) > -6:
            for count in range(7):
                if x_player_dice['ND'][count] != -1:
                    x_player_dice['ND'][count] = random.randint(1, 6)
        return x_player_dice

    def show_dice(x_dice, x_player_number):
        """x_dice对应tabletop中players里的某一玩家的['dice'] \
这里要求用过的骰子必须赋值为-1，应该在main里排除没骰子可用的情况"""
        big_dice = x_dice['SP']
        normal_dice = x_dice['ND']

        print('玩家{0}掷得了：'.format(x_player_number))
        if big_dice == -1:
            print('小骰子：', end='')
            for count in normal_dice:
                if count != -1:
                    print(count, end=' ')
        else:
            print('大骰子：{0}'.format(big_dice))
            if sum(normal_dice) > -7:
                print('小骰子：', end='')
                for count in normal_dice:
                    if count != -1:
                        print(count, end=' ')
        print()

    def select_dice(x_dice):
        """这个方法不能使用在多人模式中（包括了input）\n
        x_dice对应tabletop中players里的某一玩家的['dice']，此部分要求传入的x_dice不能全为-1，如果没有可用的骰子，应在main中予以排除"""
        valid_number = []
        if x_dice['SP'] > 0:
            valid_number.append(x_dice['SP'])
        if sum(x_dice['ND']) > -7:
            for count in x_dice['ND']:
                if count > -1:
                    valid_number.append(count)
        # 这个valid_number应该还会有别的用
        valid_number = set(valid_number)
        valid_number = list(valid_number)
        counti = 0
        while True:
            if len(valid_number) == 1:
                print('你没得选，只好选择了{0}'.format(valid_number[0]))
                return valid_number[0]
            print('选择一个掷得的骰子点数：')
            number_selected = input('-->')
            number_selected = ord(LV_Assistant.number_check(number_selected))
            number_selected = number_selected % 6
            number_selected = 6 if number_selected == 0 else number_selected
            if number_selected in valid_number:
                print('选择了{0}'.format(number_selected))
                return number_selected
            else:
                print('不正确的选择，请重选，多次重选会带来严重后果：')
                print('可供选择的数字为：', end='')
                for countj in valid_number:
                    print(countj, end=' ')
                print()
            if counti > 9:
                print('你不对劲')
                number_selected = valid_number[0]
                print('选择了{0}'.format(number_selected))
                return number_selected
            counti += 1

    def pigeon_coo(x_end=''):
        print('咕咕咕', end=x_end)

    def show_casinos(x_casinos, x_player_number):
        """传入的x_casinos应当就是tabletop.casinos"""
        for number in range(1, 7):
            print('赌场{0}上的钞票情况是：'.format(number), end='')
            for item in range(5):
                if x_casinos[number]['banknotes'][item] == 0:
                    break
                print(x_casinos[number]['banknotes'][item], end=' ')
            print('\n玩家在赌场{0}的置放情况是：'.format(number))
            for item in range(1, x_player_number + 1):
                print('玩家{0}放了{1}个；'.format(item, x_casinos[number]['player' + str(item)]), end='\t')
            print()

    def show_money(x_players):
        '''x_players应当是game_players.players'''
        print('看看谁最孙子：')
        msg = '看看谁最孙子：\n'
        for item in x_players:
            print('玩家{0}有金钱{1}货币单位'.format(item, x_players[item]['money']))
            msg += '玩家{0}有金钱{1}货币单位\n'.format(item, x_players[item]['money'])
        return msg

    def gamble_summary(x_players):
        '''x_players应当是game_players.players'''
        print('赌局终了，结果是：')
        msg = '赌局终了，结果是：\n'
        summary = []
        for item in x_players:
            summary.append((item, x_players[item]['money']))
            print('玩家{0}有金钱{1}货币单位'.format(summary[-1][0], summary[-1][1]))
            msg += '玩家{0}有金钱{1}货币单位\n'.format(summary[-1][0], summary[-1][1])
        summary = sorted(summary, key=lambda y: -y[1])

        print('玩家{0}有金钱{1}，他是孙子王'.format(summary[0][0], summary[0][1]))
        msg += '玩家{0}有金钱{1}，他是孙子王\n'.format(summary[0][0], summary[0][1])
        return msg

    def select_dice_MP(x_dice, client_socket):
        """这个方法只能使用在多人模式中（包括了input）\n
        x_dice对应tabletop中players里的某一玩家的['dice']，此部分要求传入的x_dice不能全为-1，如果没有可用的骰子，应在main中予以排除\n
        client_socket是目标玩家的传输通道"""
        valid_number = []
        if x_dice['SP'] > 0:
            valid_number.append(x_dice['SP'])
        if sum(x_dice['ND']) > -7:
            for count in x_dice['ND']:
                if count > -1:
                    valid_number.append(count)
        # 这个valid_number应该还会有别的用
        valid_number = set(valid_number)
        valid_number = list(valid_number)
        counti = 0
        while True:
            if len(valid_number) == 1:
                msgout = '你没得选，只好选择了{0}'.format(valid_number[0])
                print(msgout)
                client_socket.send(msgout.encode())
                return valid_number[0]
            msgout = '选择一个掷得的骰子点数：LVIN'
            print(msgout)
            client_socket.send(msgout.encode())
            msgin = client_socket.recv(768)
            msgin = msgin.decode()

            number_selected = ord(LV_Assistant.number_check(msgin))
            number_selected = number_selected % 6
            number_selected = 6 if number_selected == 0 else number_selected
            if number_selected in valid_number:
                msgout = '选择了{0}'.format(number_selected)
                print(msgout)
                client_socket.send(msgout.encode())
                return number_selected
            else:
                msgout = '不正确的选择，请重选，多次重选会带来严重后果：\n可供选择的数字为：\n'
                for countj in valid_number:
                    msgout += str(countj) + ' '
                msgout += '\n'
                print(msgout)
                client_socket.send(msgout.encode())
            if counti > 9:
                msgout = '你不对劲\n'
                number_selected = valid_number[0]
                msgout += '选择了{0}'.format(number_selected)
                print(msgout)
                client_socket.send(msgout.encode())
                return number_selected
            counti += 1

    def roll_dice_MP(x_player_dice, client):
        """用于多人游戏模式\n
        用来掷骰子，传入的x_player_dice应该为特定玩家的仅含{'SP': ?, 'ND': [?,?,?,?,?,?,?]}的字典，
                这里要求用过的骰子必须赋值-1"""
        if x_player_dice['SP'] + sum(x_player_dice['ND']) < -7:
            msgout = '但你没有可用的骰子'
            print(msgout)
            client.send(msgout.encode())
            return x_player_dice
        if x_player_dice['SP'] != -1:
            x_player_dice['SP'] = random.randint(1, 6)
        if sum(x_player_dice['ND']) > -6:
            for count in range(7):
                if x_player_dice['ND'][count] != -1:
                    x_player_dice['ND'][count] = random.randint(1, 6)
        return x_player_dice

    def show_casinos_MP(x_casinos, x_player_number):
        """用于多人游戏模式\n
        传入的x_casinos应当就是tabletop.casinos"""
        msg = ''
        for number in range(1, 7):
            msg += '赌场{0}上的钞票情况是：'.format(number)
            print('赌场{0}上的钞票情况是：'.format(number), end='')
            for item in range(5):
                if x_casinos[number]['banknotes'][item] == 0:
                    break
                print(x_casinos[number]['banknotes'][item], end=' ')
                msg += str(x_casinos[number]['banknotes'][item]) + ' '
            print('\n玩家在赌场{0}的置放情况是：'.format(number))
            msg += '\n玩家在赌场{0}的置放情况是：\n'.format(number)
            for item in range(1, x_player_number + 1):
                print('玩家{0}放了{1}个；'.format(item, x_casinos[number]['player' + str(item)]), end='\t')
                msg += '玩家{0}放了{1}个；\t'.format(item, x_casinos[number]['player' + str(item)])
            print()
            msg += '\n'
        return msg

    def show_dice_MP(x_dice, x_player_number):
        """x_dice对应tabletop中players里的某一玩家的['dice'] \
    这里要求用过的骰子必须赋值为-1，应该在main里排除没骰子可用的情况"""
        big_dice = x_dice['SP']
        normal_dice = x_dice['ND']

        print('玩家{0}掷得了：'.format(x_player_number))
        msg = '玩家{0}掷得了：\n'.format(x_player_number)
        if big_dice == -1:
            print('小骰子：', end='')
            msg += '小骰子：'
            for count in normal_dice:
                if count != -1:
                    print(count, end=' ')
                    msg += str(count) + ' '
        else:
            print('大骰子：{0}'.format(big_dice))
            msg += '大骰子：{0}\n'.format(big_dice)
            if sum(normal_dice) > -7:
                print('小骰子：', end='')
                msg += '小骰子：'
                for count in normal_dice:
                    if count != -1:
                        print(count, end=' ')
                        msg += str(count) + ' '
        print()
        msg += '\n'
        return msg

    def show_casinos_MP_GUI(x_casinos, x_player_number):
        """用于多人游戏模式\n
        传入的x_casinos应当就是tabletop.casinos"""
        msg = ''
        for number in range(1, 7):
            msg += '赌场{0}上的钞票情况是：'.format(number)
            print('赌场{0}上的钞票情况是：'.format(number), end='')
            for item in range(5):
                if x_casinos[number]['banknotes'][item] == 0:
                    break
                print(x_casinos[number]['banknotes'][item], end=' ')
                msg += str(x_casinos[number]['banknotes'][item]) + ' '
            print('\n玩家在赌场{0}的置放情况是：'.format(number))
            msg += 'CINFO\n玩家在赌场{0}的置放情况是：\n'.format(number)
            for item in range(1, x_player_number + 1):
                print('玩家{0}放了{1}个；'.format(item, x_casinos[number]['player' + str(item)]), end='\t')
                msg += '玩家{0}放了{1}个；\t'.format(item, x_casinos[number]['player' + str(item)])
            print()
            msg += 'PINFO\n'
        return msg

    def __init__(self):
        '''不要实例化LV_Assistant'''
        print('不要实例化LV_Assistant')


if __name__ == '__main__':
    A = {'SP': 5, 'ND': [4, 4, -1, -1, -1, -1, -1]}
    B = LV_Assistant.select_dice(A)
