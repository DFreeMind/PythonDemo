'''
Created on 2017年6月21日
socket客户端
@author: iBook
'''
import socket
import time


#客户端
#1.创建socket连接
#2.连接服务端
#3.接收数据
socket_client = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
#连接客户端
socket_client.connect(("127.0.0.1",9487))
#接收服务端数据,需要解码
data = socket_client.recv(1024)
print(data)
#将byte数组转成字符串
print(data.decode("utf-8"))

#向服务端发送数据
socket_client.send("waiting for rev".encode(encoding='utf_8', errors='strict'))

#循环接收服务端数据
while True:
    data = socket_client.recv(1024).decode("utf-8")
    if data != '':
        print(data)
    socket_client.send((data + "哈").encode("utf-8"))
    time.sleep(1)











