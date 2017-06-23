'''
Created on 2017年6月22日
BeautifulSoup需要安装
快速获取html或xml文章中的数据
安装:pip install beautifulSoup4
@author: iBook
'''
#select选择器
#通过标签、class、id查找、判断某个标签是否有某个属性
import urllib.request
from bs4 import BeautifulSoup


url = "http://www.weduoo.com"
content = urllib.request.urlopen(url).read().decode("utf-8")
soup = BeautifulSoup(content)
#返回一个list
title = soup.select("title")
#获取标签的值通过.string获取
text = title[0].string
print(title)

#级联查找
a_list = soup.select("body a")
print(a_list)











