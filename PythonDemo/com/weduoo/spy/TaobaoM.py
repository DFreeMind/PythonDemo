'''
Created on 2017年6月23日
抓取淘宝MM照片
@author: iBook
'''
#淘宝美人库地址
import urllib.request


url = "https://mm.taobao.com/search_tstar_model.htm?spm=5679.126488.640745.2.OrbDBW"
#打开首页
resp = urllib.request.urlopen(url)
