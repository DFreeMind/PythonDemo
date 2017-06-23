'''
Created on 2017年6月21日

@author: iBook
'''
import urllib.request


url = "http://www.baidu.com"
#get的第一种方式
res = urllib.request.urlopen(url)
if res.status ==200:
    data1 = res.read().decode("utf-8")
#     print(data)

#get的第二种方式
req= urllib.request.Request(url)
res2 = urllib.request.urlopen(req)
if res2.status ==200:
    data2 = res2.read().decode("utf-8")
#     print(data)


#post请求
data = {"name":"weduoo","age":"22"}
#对传入的数据进行编解码
z_data = urllib.parse.urlencode(data)
req3 = urllib.request.Request(url,z_data.encode('utf_8'))
res3 = urllib.request.urlopen(req3)
if res3.status ==200:
    data3 = res3.read().decode("utf-8")
#     print(data3)


#header请求
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"

values = {
        'name': 'Michael Foord',
        'location' : 'Northampton',
        'language' : 'Python'
    }
headers = {'user-agent' : user_agent}
data4 = urllib.parse.urlencode(values)
req4 = urllib.request.Request(url,data4.encode(encoding='utf_8'),headers)
res4 = urllib.request.urlopen(req4)
the_page = res4.read().decode('utf-8')
print(the_page)


















