'''
Created on 2017年6月23日
抓取淘宝MM照片
@author: iBook
'''
#淘宝美人库地址
import json
import os
import urllib.request

from bs4 import BeautifulSoup


path = "F:/models/"

#MM主页URL
base_url = "https://mm.taobao.com/self/aiShow.htm?userId="

#获取MM基本信息的URL
models_url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"

#打开首页
def search_models(index):
    page = index
    while page < 14:
        print(page)
        data = {
                "q":"",
                "viewFlag":"A",
                "sortType":"default",
                "searchStyle":"",
                "searchRegion":"city:",
                "searchFansNum":"",
                "currentPage":page,
                "pageSize":100
                }
        #对参数编码
        z_data = urllib.parse.urlencode(data)
        req = urllib.request.Request(url = models_url,data = z_data.encode("utf-8"))
        resp = urllib.request.urlopen(req)
        models_data = resp.read().decode("gbk")
        models_list = get_models_info(models_data)
        for_url_save(models_list)
        page += 1
        
        
#解析返回的Models的信息,姓名,主页ID,年龄等
def get_models_info(models_data):
    data = json.loads(models_data)
    print(data)
    #解析返回的MM JSON数据
    data_1 = data.get("data")
    searchDOList=data_1.get("searchDOList")
    models_list = list()
    for info in searchDOList:
        model_name = info.get("realName")
        model_id=info.get("userId")
        print(model_name)
        print(model_id)
        models_list.append((model_name,model_id))
    return models_list
       

#访问model的主页,爬出图片
def get_models_pic(t):
    resp = urllib.request.urlopen(base_url+str(t[1]))
    models_index = resp.read().decode("gbk")
    soup = BeautifulSoup(models_index)
    imgs_url = soup.select("img[src]")
    imgs_list = list()
    for img in imgs_url:
        #图片资源过滤
        src = img["src"]
        #,没有下划线的话图片较大
        if "!!0-tstar.jpg_" in src:
            imgs_list.append(src)
    return t[0],t[1],imgs_list    

#创建文件夹
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

#保存图片
def saveImg(imageURL,fileName):
        u = urllib.request.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        print("正在保存mm图片" + fileName)
        f.write(data)
        f.close()

#遍历url保存图片
def for_url_save(models_list):
    for t in models_list:
        model_name,model_id,imgs_list = get_models_pic(t)
        m_path = path+model_name #+ "-" + str(model_id)
        mkdir(m_path)
        index = 0
        for img in imgs_list:
            print(img)
            saveImg("https:" + img, m_path+"/" + model_name +str(index)+".jpg")
            index += 1

if __name__ == '__main__':
    search_models(3)




