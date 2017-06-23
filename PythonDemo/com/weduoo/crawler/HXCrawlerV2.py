'''
Created on 2017年6月22日
虎嗅网爬虫
    1.解析首页

建表语句
DROP TABLE IF EXISTS `python_huxiu_article`;

CREATE TABLE `python_huxiu_article` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `share` varchar(11) DEFAULT NULL,
  `zan` varchar(11) DEFAULT NULL,
  `pl` varchar(11) DEFAULT NULL,
  `time` varchar(50) NOT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=574 DEFAULT CHARSET=utf8;

-----------------------

V2:添加分页公能
1.现请求首页,在首页中拿到 data-last_dateline
2.分页API:https://www.huxiu.com/v2_action/article_list
3.分页API参数:
    huxiu_hash_code:207c09b4b1fa597415da13c73912ccc8
    page:2
    last_dateline:1498034520
4.cookie的变化,分页请求都会返回cookie,下次七请求会携带发到服务器

使用到技术
1.urllib的post请求: urllib.request.Request
2.对请求进行编码:urllib.parse.urlencode
3.添加header头,伪造浏览器信息,向服务器发送SERVERID

@author: iBook
'''
import json
import urllib.parse
import urllib.request

import MySQLdb
from bs4 import BeautifulSoup

#获取SERVERID的方法
def get_server_id(headers):
    print(headers)
    for header_tuple in headers:
        index_0 = header_tuple[0]
        index_1 = header_tuple[1]
        if index_0 == "Set-Cookie" and "SERVERID" in index_1:
            return index_1.split(";")[0]
        

def get_article_urls(soup):
    #2.查询所有a标签的url
    a_list = soup.select("a[href]")
    #定义一个set存储所有返回的url
    url_set = set()
    for a_tag in a_list:
        #获取标签中的值
        href = a_tag["href"]
        #print(href)
        if "article" in href and "http" not in href and "/1.html" not in href and "video" not in href:
            #去掉重复的url
            url_set.add(href)
    return url_set

   
#爬虫分为两类 : 垂直爬虫(针对某给网站)与通用爬虫(百度等)
#定义一个公共的解析方法
def parse_index_page():
    url = "https://www.huxiu.com"
    #解析首页的新闻
    #主要a标签中含有article属性就是新闻
    resq= urllib.request.urlopen(url)
    
    #获取SERVERID
    headers = resq.getheaders()
    server_id = get_server_id(headers)
    
    index_page = resq.read().decode('utf-8')
    
    #解析
    #1.创建beautifulSoup,解析last_dateline
    soup = BeautifulSoup(index_page)
    
    #使用class解析时不能有空格
    last_dateline_tags = soup.select("div[data-last_dateline]")
    last_dateline_tag = last_dateline_tags[0]  
    last_dateline = last_dateline_tag["data-last_dateline"]
    print("请求时间:" + last_dateline )
    
    #返回一个元组,时间和url集合
    return server_id,last_dateline,get_article_urls(soup)

#解析文章信息,传入url集合
def parse_article(url_set):
    #存放所有文章的信息
    article_list = list()
    for url in url_set:
        #用于反爬虫机制
        #import time
        #time.sleep(10)
        url = "https://www.huxiu.com" + url
        print("网址 : " + url)
        #访问url
        the_page = urllib.request.urlopen(url)
        #解析网站内容
        #标题、内容、搜藏、评论、点赞、时间
        page_soup = BeautifulSoup(the_page)
        title = page_soup.select(".t-h1")[0].string
        print("标题 :" + title)
        
        time = page_soup.select(".article-time")[0].string
        print("时间:" + time)
        
        share = page_soup.select(".article-share")[0].string
        print("搜藏:" + share)
        
        pl = page_soup.select(".article-pl")[0].string
        print("评论:" + pl)
 
        num_list = page_soup.select(".num")
        if len(num_list) > 0:
            num = num_list[0].string
        else:
            num = "评论0"
        print("点赞:" + num)
        
        #获取文章内容,只获取文本信息
        content = page_soup.select(".article-content-wrap")
        p_list = content[0].select("p")
        #文章信息
        content_value = "";
        for p in p_list:
            #过滤掉不需要的信息,作者/出品/设计等信息
            span_list = p.select("span[class=text-remarks]")
            if len(span_list) > 0:
                continue
            p_value = p.string
            if p_value == None or p == "":
                continue
            content_value = content_value + p_value +"\r\n"
        print("内容:" + content_value )
        article_list.append((url,title,share,pl,num,time,content_value))
    return article_list

#保存到mysql

def sava_article_info(article_list):
    #保存数据到mysql,需要制定数据库字符集
    db = MySQLdb.connect("localhost","root","1234","test",charset="utf8")
    cursor = db.cursor()
    #执行多条插入
    sql = "INSERT INTO `test`.`python_huxiu_article` (`url`, `title`, `share`, `pl`, `zan`, `time`, `content`) VALUES ( %s, %s, %s, %s, %s, %s, %s);"
    cursor.executemany(sql,article_list)
    #关闭
    cursor.close()
    db.commit()


#更新SERVERID,去掉原来的,换成最新的
def update_headers(headers, server_id):
    cookies = headers["Cookie"]
    cookie_str = ""
    for cookie in cookies.split(";"):
        if "SERVERID" not in cookie:
            cookie_str = cookie_str + cookie + ";"
    cookie_str = cookie_str + server_id
    headers["Cookie"] = cookie_str    
    return headers

#3.分页请求
def do_padeing(last_dateline,server_id):
    page = 1 #首页
    while page < 1071:
        page += 1
        url = "https://www.huxiu.com/v2_action/article_list"
        #请求参数
        data = {
                 "huxiu_hash_code":"207c09b4b1fa597415da13c73912ccc8",
                 "page":page,
                 "last_dateline":last_dateline
            }
        #对参数编码
        z_data = urllib.parse.urlencode(data)
        headers = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                #与utf-8编码有冲突
                #"Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Connection":"keep-alive",
                "Content-Length":"80",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie":"huxiu_analyzer_wcy_id=46ks8mvv5w5aeetr43ec; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22158ce3ac49262a-0c7039d98a4594-581c3915-1fa400-158ce3ac4935bd%22%7D; aliyungf_tc=AQAAAHahdCa76AUAU3Awtv5W62x+1QSC; PHPSESSID=aaujd29e9ajgb7nt569npmdcn4; _ga=GA1.2.1177189611.1480928707; _gat=1; Hm_lvt_324368ef52596457d064ca5db8c6618e=1482200680,1482202286,1482724863,1482751993; Hm_lpvt_324368ef52596457d064ca5db8c6618e=1482755006; screen=%7B%22w%22%3A1920%2C%22h%22%3A1080%2C%22d%22%3A1%7D; SERVERID=03a07aad3597ca2bb83bc3f5ca3decf7|1482755272|1482751991",
                "Host":"www.huxiu.com",
                "Origin":"https//www.huxiu.com",
                "Referer":"https//www.huxiu.com/",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
                "X-Requested-With":"XMLHttpRequest"
            }
        #请求数据
        req = urllib.request.Request(url = url,data = z_data.encode("utf-8"),headers = update_headers(headers,server_id))

        #获取分页分返回的数据
        resp = urllib.request.urlopen(req)
        
        #获取新的Headers
        server_id = get_server_id(resp.getheaders())
        
        #解析json
        json_str = resp.read().decode('utf-8')
        resp_data = json.loads(json_str)
        data = resp_data.get("data")
        last_dateline = resp_data.get("last_dateline")
        
        url_set = get_article_urls(BeautifulSoup(data))
        
        #1.解析url_set
        article_list = parse_article(url_set)
        #2.将文章保存到数据库
        sava_article_info(article_list)

if __name__ == '__main__':
    #首页url解析
    server_id,last_dateline,url_set = parse_index_page()
    print(last_dateline)
    print(server_id)
    #分页请求,解析url_set,使用多线程去处理
    do_padeing(last_dateline, server_id)
    
    
    
    
    
    
    
