'''
Created on 2017年6月25日
文件相关操作
@author: weduoo
'''
import os


path="../logs/taomm_.log"


#普安顿taomm日志路径是否存在，不存在则创建文件
def write_taomm():
    log_file = open(path,"a",encoding="utf-8")
    log_file.write('362438816' + "\t" + "尚洁" + "\n") 
    log_file.close()
    
def read_taomm_line():
    read_taomm = open(path,"r",encoding="utf-8")
    models = list()
    for line in read_taomm.readlines():
        li = line.split("\t")
        models.append(li[0])
        print(models)
    if 362438816 in models:
        print("yes")
    else:
        print("no")
    
    
if __name__ == '__main__':
    #write_taomm()
    #read_taomm_line()
    a = list()
    a.append(1)
    a.append(2)
    a.append(1)
    print(a)
    print(max(a))




