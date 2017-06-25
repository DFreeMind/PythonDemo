'''
Created on 2017年6月20日

@author: iBook
'''
#读写文件
#读文件 open(路径,读取的方式[r(read读),w(write覆盖写),a(append追加)])
from _collections import deque, OrderedDict
from collections import namedtuple, Counter
from datetime import datetime, timedelta

"""
 open操作的几种读写模式
 
'r'       open for reading (default)
'w'       open for writing, truncating the file first
'x'       create a new file and open it for writing
'a'       open for writing, appending to the end of the file if it exists
'b'       binary mode
't'       text mode (default)
'+'       open a disk filÅe for updating (reading and writing)Å
'U'       universal newline mode (deprecated)
"""
path = "D://temp.txt"
#读时指定编码格式
f = open(path,"r",encoding="utf-8")
data = f.read()
print(data)
f.close()

#行读取文件
path2 = "D://temp.txt"
f2 = open(path2,"r",encoding="utf-8")
for line in f2.readlines():
    print("----------->" + line)
f2.close()

#写入文件,通过utf8的形式写入
path3 = "D://temp.txt"
f3 = open(path3,"w",encoding="utf-8")
f3.write("我爱你")
f3.close()

#追加写
path4 = "D://temp.txt"
f4 = open(path4,"a",encoding="utf-8")
#指定换行符
f4.write("\n")
f4.write("我也爱你呀")
f4.close()


#文件读写异常处理
try:
    path5 = "D://temp.txt"
    f5 = open(path5,"r",encoding="utf-8")
    for line in f5.readlines():
        print(line)
finally:
    f5.close()

#异常处理的简单写法
with open(path5,"r",encoding="utf-8") as f:
    print(f.readlines())


'''
时间操作
    1.date固定格式字符串
    2.字符串转date
'''
now = datetime.now()
#2017-06-20 16:27:10.405836      
print(now)
#转格式
str_time = now.strftime("%Y-%m-%d %H:%M:%S")
print(str_time)

#字符串转时间
date = datetime.strptime("20170620 16:27:10","%Y%m%d %H:%M:%S")
print(date)

#对日期进行加减操作
now = datetime.now()
#加小时
now = now + timedelta(hours = 2)
print(now)
#加天
now = now + timedelta(days = 2)
print(now)


'''
对集合增强
    1.Namedtuple
    2.deque:相当于java中的linkedlist,查询满,删除修改快
    3.ordereddict:key会按照插入的顺序排列
    4.counter: 简单计数器
'''
#1.namedtuple
t = ("name","age","sex")
t[0] #通过角标获取

#作为一个单独的数据结构,每个元素都有名称
Per = namedtuple("Per",["name","age","sex"])
p = Per("weduoo","24","male")
print(p.name)

#2.deque
linked = deque([1,2,3,4])
#弹出元素
item = linked.pop()
print(item)
print(linked)
linked.popleft()
print(linked)

#添加一个元素
linked.append(4)
print(linked)
linked.appendleft(1)
print(linked)

#3. ordereddict,按照key插入的顺序排列
od = OrderedDict([("a",1),("c",3),("b",2)])
for item in od.items():
    print(item)


#4. counter 简单计数
counter = Counter()
str = "asdfad"
for ch in str:
    counter[ch] = counter[ch] + 1
print(counter)









