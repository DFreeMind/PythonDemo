'''
Created on 2017年6月20日

@author: iBook
'''
# 在Python中如果一个类没有直接父类,那么参数就写object
from builtins import int
class Person(object):
    # Python中欧init方法相当于构造器
    # 参数列表中第一个位置是一个默认的叫做self,也就是实例本身,相当于java的this 
    def __init__(self, name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
    
    #定义一个方法
    def running(self):
        print(self.name + "你别跑")

#继承:将集成的类放到括号中
class Rich(Person):
    pass

#多态
# Python中多态是伪多态,是鸭子类型,只要走路像鸭子,就是鸭子
# 只要传入参数有这个方法就可以.
# Python对类没有严格的类型检测
class ItRich(object):
    def printInfo(self,rich):
        rich.running()
    
#定义出函数
# if __name__ == '__main__':
#         #创建实例
#         #preson = Person("鸣人 ", 18, "male")    
#         #preson.running()
#         rich = Rich("高富帅", 26, "男")
#         #rich.running()
#         it = ItRich()
#         it.printInfo(rich)

'''
    获取类的信息(相当于java中的反射)
    1.获取一个变量的类型
    2.比较变量的类型
    3.查看类型的方法
    4.查看类的属性
'''
def aaa():
    pass

if __name__ == '__main__':
    f = aaa()
    print(type(f))
    
    #判断变量的类型
    i = 0
    r = isinstance(i, int)
    print(r)
    
    print(type("add") == str)
    
    #dir:获取类的属性和方法,返回包含字符串的list
    #带下划线的是内部方法
    #['__class__', '__delattr__', '__dict__', '__dir__',
    # '__doc__', '__eq__', '__format__', '__ge__', 
    #'__getattribute__', '__gt__', '__hash__', '__init__',
    # '__le__', '__lt__', '__module__', '__ne__', '__new__',
    # '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
    # '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'running']

    print(dir(Person))
    
    #操作一个对象的状态
    #getattr()、setattr()、hasattr()
    #getattr获取对象的属性的值
    p = Person("名字","年龄","性别")
    r1 = getattr(p, "age", 18) 
    print(r1)
    r1 = getattr(p, "age1", 18) 
    print(r1)
    
    
    















        
    