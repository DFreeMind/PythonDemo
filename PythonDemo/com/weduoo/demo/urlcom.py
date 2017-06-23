'''
Created on 2017年6月21日
简单爬虫
@author: iBook
'''
#3.x的导包
import socket
import threading
import urllib.parse
import urllib.request


#百度首页
url = "http://www.baidu.com"
#发起请求,得到返回对象
res = urllib.request.urlopen(url)
#查看返回状态,是200则解析返回的数据
if res.status == 200:
    print("succees")
    #获取数据,并指定编码集
    data = res.read().decode("utf-8")
#     print(data)
#     soup = BeautifulSoup(data)
#     print(soup.title)
















    