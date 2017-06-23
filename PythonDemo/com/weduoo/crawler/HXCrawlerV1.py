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

@author: iBook
'''
import urllib.request
from bs4 import BeautifulSoup
import MySQLdb

#爬虫分为两类 : 垂直爬虫(针对某给网站)与通用爬虫(百度等)

#定义一个公共的解析方法
def parse_index_page():
    url = "https://www.huxiu.com"
    #解析首页的新闻
    #主要a标签中含有article属性就是新闻
    index_page = urllib.request.urlopen(url).read().decode('utf-8')
    #print(index_page)
    
    #解析
    #1.创建beautifulSoup
    soup = BeautifulSoup(index_page)
    
    #2.查询所有a标签的url
    a_list = soup.select("a[href]")
    #定义一个set存储所有返回的url
    url_set = set()
    for a_tag in a_list:
        #获取标签中的值
        href = a_tag["href"]
        #print(href)
        if "article" in href and "http" not in href and "1.html" not in href and "video" not in href:
            #去掉重复的url
            url_set.add(href)
    return url_set

#解析文章信息,传入url集合
def parse_article(url_set):
    #存放所有文章的信息
    article_list = list()
    for url in url_set:
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

if __name__ == '__main__':
    #首页url解析
    url_set = parse_index_page()
    #单个文章解析
    article_list = parse_article(url_set)
    #将文章保存到数据库
    sava_article_info(article_list)
    
    
    
    
