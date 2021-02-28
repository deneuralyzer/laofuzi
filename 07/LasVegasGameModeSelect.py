class LV_Game_Mode_Select:
    '''模式选择模块，0为重选，1为单机，2为云单机，3为联机多人'''
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

# A = LV_Game_Mode_Select()
