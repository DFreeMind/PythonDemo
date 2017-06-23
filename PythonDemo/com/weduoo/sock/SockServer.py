'''
Created on 2017年6月21日

@author: iBook
'''
from _ast import If
'''
网络编程
    1.TCP
    2.UDP
'''
#tcp编程
#1.服务端
# >.socket.socket()
# >.绑定地址和端口号
# >.监听客户端
# >.接受客户端请求
#family=AF_INET  : 地址族,IP地址类型(IPv4/IPv6),
#    AF: Address Family 
#    INET: inetnet
#    AF_INET : IPv4
#    AF_INET6 : IPv6
#type=SOCK_STREAM: 数据传输方式
#    SOCK_STREAM: 面向连接传输方式,数据可以准确到达另一侧,数据丢失就会重新发送
#    SOCK_DGRAM: 无连接的传输方式,不做数据校验,相对较快
#proto=0 : 表示传输协议,一般有TCP和UDP

import socket
import threading


def run(sock, addr):
    print(addr)
    #发送bytes数组
    sock.send("success".encode(encoding='utf-8'))
    
    #循环接收客户端发送的数据
    while True:
        data = sock.recv(1024).decode("utf-8")
        if data != '':
            print(data)
        sock.send((data + "嘿").encode("utf-8"))
    
    
    

#创建服务
socket_server = socket.socket(family = socket.AF_INET,type = socket.SOCK_STREAM)
#绑定地址
socket_server.bind(("127.0.0.1",9487))
#进入监听状态
socket_server.listen()

#循环接收请求
while True:
    #接受一个请求
    #sock 表示网络通道,用于数据读取
    #addr 表示客户端的ip地址
    (sock,addr) = socket_server.accept()
    thread = threading.Thread(target=run,name="模拟",args=(sock,addr))
    #启动线程
    thread.start()