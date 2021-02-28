class LV_Settlement:
    '''用于结算'''
    def check_duplicate(x_casinos, x_player_number):
        '''x_casinos就是tabletop.casinos'''
        msg = ''
        for number_i in x_casinos:
            for number_j in range(1, x_player_number + 1):
                if x_casinos[number_i]['player' + str(number_j)] == 0:
                    continue
                temp_number = x_casinos[number_i]['player' + str(number_j)]
                temp_player = number_j
                for number_k in range(number_j + 1, x_player_number + 1):
                    if x_casinos[number_i]['player' + str(number_k)] == 0:
                        continue
                    if x_casinos[number_i]['player' + str(number_k)] == temp_number:
                        x_casinos[number_i]['player' + str(number_j)] = 0
                        x_casinos[number_i]['player' + str(number_k)] = 0
                        print('玩家{0}和{1}在赌场{2}有相同骰子数{3}'.format(number_j, number_k, number_i, temp_number))
                        msg += '玩家{0}和{1}在赌场{2}有相同骰子数{3}\n'.format(number_j, number_k, number_i, temp_number)
        return msg

    def comparison(x_casinos, x_player_number):
        '''doc'''
        compared = []
        for number_i in x_casinos:
            compared.append([])
            for number_j in range(1, x_player_number + 1):
                temp = (number_j, x_casinos[number_i]['player' + str(number_j)])
                compared[-1].append(temp)

            
            compared[-1] = sorted(compared[-1], key = lambda y : -y[1])
            # print(compared)
        return compared

    def money_assignment(x_compared, x_casinos, x_players, x_player_number):
        '''这里的x_compared是comparison里返回的compared'''
        msg = ''
        # 遍历赌场
        for number_i in range(6):
            # counter是casino[赌场号]['banknotes']的位置
            counter = 0
            for number_j in range(1, x_player_number + 1):
                # 如果赌场上玩家的骰子数量不为0
                # 这个从0开始和从1开始是挺烦
                if x_compared[number_i][number_j - 1][1] != 0:
                    # 发送给哪个玩家
                    # 赌场counter位置的钱数不为空
                    if x_casinos[number_i + 1]['banknotes'][counter] != 0:
                        to_player = x_compared[number_i][number_j - 1][0]
                        how_much = x_casinos[number_i + 1]['banknotes'][counter]
                        x_casinos[number_i + 1]['banknotes'][counter] = 0
                        x_casinos[number_i + 1]['total_notes'] -= how_much
                        x_players[to_player]['money'] += how_much
                        counter += 1
                        print('玩家{0}从赌场{1}拿到{2}（货币单位）'.format(to_player, number_i + 1, how_much))
                        print('玩家{0}牛了'.format(to_player))
                        msg += '玩家{0}从赌场{1}拿到{2}（货币单位），牛了\n'.format(to_player, number_i + 1, how_much)
        return msg

# players = {1:{ 'dice': {}, 'money':0}, 2:{'dice':{}, 'money':0}, 3:{'dice':{}, 'money':0}}
# casinos = {1: {'banknotes': [6, 0, 0, 0, 0], 'total_notes': 6, 'player1': 2, 'player2': 3, 'player3': 2}, 2: {'banknotes': [10, 0, 0, 0, 0], 'total_notes': 10, 'player1': 2, 'player2': 1, 'player3': 0}, 3: {'banknotes': [10, 2, 0, 0, 0], 'total_notes': 12, 'player1': 0, 'player2': 2, 'player3': 2}, 4: {'banknotes': [6, 3, 0, 0, 0], 'total_notes': 9, 'player1': 0, 'player2': 0, 'player3': 0}, 5: {'banknotes': [6, 0, 0, 0, 0], 'total_notes': 6, 'player1': 1, 'player2': 0, 'player3': 0}, 6: {'banknotes': [9, 2, 0, 0, 0], 'total_notes': 9, 'player1': 2, 'player2': 0, 'player3': 3}}
