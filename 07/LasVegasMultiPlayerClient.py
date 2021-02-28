# LasVegasMultiplayer对应的客户端
import socket
import threading
import multiprocessing
import queue
import re
import time


def bd(protocol, port):
    protocol.bind(('', port))


def udpsend(protocol, IPaddr):
    protocol.sendto('LasVegas'.encode(), (IPaddr, 20211))

def tcpconn(protocol, IPaddr):
    protocol.connect((IPaddr, 20201))
    print('正在连接')

def tcprecv(tcpSock, Q):
    while True:
        msg = tcpSock.recv(1024)
        Q.put(msg.decode('utf-8', 'ignore'))
        # print(msg.decode())

def instructions(protocol, Q):
    CONDITION_IN = re.compile('LVIN$')
    while True:
        if Q.qsize() > 0:
            msg = Q.get()

            result = CONDITION_IN.search(msg)

            if not result:
                print(msg)
            else:
                print(msg[:-4])
                tcpsend(protocol)

def tcpsend(protocol):
    while True:
        content = input('-->')
        content = str(content)
        if content:
            content = content[0]
            protocol.send(content.encode())
            break
        else:
            print('不正常的数字，需要重新输入：\n-->')

if __name__ == '__main__':
    # UDP使用20210端口发送
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    trd1 = threading.Thread(target=bd, args=(udp, 20210))
    trd1.start()
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trd1.join()
    trd1 = threading.Thread(target=bd, args=(tcp, 20200))
    trd1.start()


    serverIP = input('输入服务器IP地址（这里将不检测你的IP地址是否合规，填错了必玩不了）：\n-->')
    trd1 = threading.Thread(target=udpsend, args=(udp, serverIP))
    trd1.start()
    print('连接服务器')
    msgQ = queue.Queue()

    trd2 = threading.Thread(target=tcpconn, args=(tcp, serverIP))
    trd2.start()
    trd2.join() # conn的太慢后面的代码先进行了就报错
    pos1 = threading.Thread(target=tcprecv, args=(tcp, msgQ))
    pos1.start()
    pos2 = threading.Thread(target=instructions, args=(tcp, msgQ))
    pos2.start()
    pos1.join()
    pos2.join()
    print('?Client End')




