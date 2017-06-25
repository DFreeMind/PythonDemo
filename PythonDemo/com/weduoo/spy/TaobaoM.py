'''
Created on 2017年6月23日
抓取淘宝MM照片
@author: weduoo
'''
#淘宝美人库地址
import json
import os
import urllib.request

from bs4 import BeautifulSoup

#爬去的照片存放位置
path = "/Users/weduoo/Crawler/modelsss/"

#已经爬出modle数据记录
taomm_log_path = "../logs/taomm.log"

#淘宝美人库地址
beatiful_path = "https://mm.taobao.com/search_tstar_model.htm"

#model主页URL
base_url = "https://mm.taobao.com/self/aiShow.htm?userId="

#获取model基本信息的URL，以JSON格式返回
models_url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"


"""
打开首页,
@param index: 表示已经读取到了那一页
@param model_history: 已经读取的model数据，不需要再次爬取
"""
def search_models(index,model_history):
    page = index
    while page < 102400:
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
        #发送请求获取model信息，以JSON格式返回
        req = urllib.request.Request(url = models_url,data = z_data.encode("utf-8"))
        resp = urllib.request.urlopen(req)
        #读取请求数据
        models_data = resp.read().decode("gbk")
        #获取model基本信息
        models_list = get_models_info(models_data)
        #解析model主页，并将图片保存，
        for_url_save(models_list,model_history,page)
        page += 1
        

'''
解析返回的Models的信息,姓名,主页ID,年龄等
数据的格式如下：
{
    "data":{
        "currentPage":2,
        "searchContents":"{viewFlag:A,searchStyle:,searchRegion:,searchFansNum:null}",
        "searchDOList":[
            {
                "avatarUrl": "//gtd.alicdn.com/sns_logo/i8/TB1o3VFQFXXXXXHXXXXSutbFXXX.jpg", 
                "cardUrl": "//img.alicdn.com/imgextra/i2/143534224/TB1cQ9kQpXXXXaTaXXXXXXXXXXX_!!0-tstar.jpg", 
                "city": "杭州市", 
                "height": "165.0", 
                "identityUrl": "", 
                "modelUrl": "", 
                "realName": "宴宴gy", 
                "totalFanNum": 0, 
                "totalFavorNum": 200594, 
                "userId": 143534224, 
                "viewFlag": "", 
                "weight": "44.0"
            }...
        ],
        "searchText":"",
        "totalCount":43476,
        "totalPage":1450
    },
    "message":"search success!",
    "status":"1"
}
'''
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
        print(model_name + "\t" +str(model_id))
        #（名字，主页id）元组添加到list中
        models_list.append((model_name,model_id))
    return models_list
       

#遍历url保存图片
def for_url_save(models_list,model_history,page):
    for t in models_list:
        #历史记录不存在则不爬取
        if not isInHistry(t[1], model_history):
            model_name,model_id,imgs_list = get_models_pic(t)
            #将以爬取的model信息保存，下次不再爬取
            save_model_history(model_id,model_name,page)
            #设置图片保存地址主路径+model名字，也可以再拼接上model id
            m_path = path+model_name #+ "-" + str(model_id)
            mkdir(m_path)
            index = 0
            for img in imgs_list:
                saveImg("https:" + img, m_path+"/" + model_name +str(index)+".jpg",page)
                index += 1
        #已存在不爬取
        else:
            print("以爬取过得model：" + t[0] + "\t" + str(t[1]))
  
          
#判断当前model的图片是否已经爬取
def isInHistry(model_id,model_history):
    if str(model_id) in model_history:
        return True
    else:
        return False


#保存已经爬取的model信息
def save_model_history(model_id,model_name,page):
    #打开历史信息文件操作
    log_file = open(taomm_log_path,"a",encoding="utf-8")
    log_file.write(str(model_id) + "\t" + model_name + "\t" + str(page) + "\n")
    log_file.close()

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
        #没有下划线的话图片较大
        if "!!0-tstar.jpg_" in src:
            imgs_list.append(src)
    return t[0],t[1],imgs_list  

#保存图片
def saveImg(imageURL,fileName,page):
    u = urllib.request.urlopen(imageURL)
    data = u.read()
    f = open(fileName, 'wb')
    print("正在保存mm图片，保存地址：" + str(page) + "\t" + fileName +"\t" + imageURL)
    f.write(data)
    f.close()

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



"""
获取读取到历史数据
@param isPage: 是否读取分页信息，读取表示下次再读取的时候从记录的页面开始，不读取则从第一页开始
"""
def get_page_model_hitory(isPage):
    #默认初始页
    page = 1
    models_history_list = list()
    isExist = os.path.exists(taomm_log_path)
    page_list=list()
    if isExist:
        data = open(taomm_log_path,"r",encoding = "utf-8")
        for line in data.readlines():
            model_page = line.split("\t")
            print(model_page)
            models_history_list.append(model_page[0])
            page_list.append(int(model_page[2]))
    if isPage:
        #获取以保存的页码最大值
        page = max(page_list)
        return page,models_history_list
    else:
        return page,models_history_list
    
#运行主方法
if __name__ == '__main__':
    page,model_history = get_page_model_hitory(True)
    search_models(page,model_history)




