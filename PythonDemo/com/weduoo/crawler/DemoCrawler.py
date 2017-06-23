'''
Created on 2017年6月22日

@author: iBook
'''
import json
import urllib.request
import urllib.parse

import MySQLdb
from bs4 import BeautifulSoup


def get_server_id(headers):
    for header_tuple in headers:
        index_0 =  header_tuple[0]
        index_1 = header_tuple[1]
        if index_0 =="Set-Cookie" and "SERVERID" in index_1:
            return index_1.split(";")[0]


def get_article_urls(soup):
    url_set = set()
    # 定义一个set 用来返回首页中所有的url
    # 查询 所有文章url 文章url都是a标签
    a_list = soup.select("a[href]")
    for a_tag in a_list:
        # 获取a标签中href属性的值
        # 获取标签中属性的值 标签["属性名称"]
        href = a_tag["href"]
        if "article" in href and "http" not in href  and "/1.html" not in href:
            print("-----------------------得到新闻URL " + href)
            url_set.add(href)
    return url_set


def parse_index_page():
    url = "https://www.huxiu.com"
    print("-----------------------爬取首页 "+url)
    # 获取虎嗅网站首页的内容
    resp = urllib.request.urlopen(url)
    #获取serverid  headers是一个list
    headers = resp.getheaders()
    server_id = get_server_id(headers)
    index_page = resp.read().decode('utf-8')
    # 解析
    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(index_page)
    #解析last_dateline
    last_dateline_tags = soup.select("div[data-last_dateline]")
    last_dateline_tag = last_dateline_tags[0]
    last_dateline = last_dateline_tag["data-last_dateline"]
    url_set = get_article_urls(soup)
    return server_id,last_dateline,url_set


def parse_article(url_set):
    article_list = list()
    for url in url_set:
        import time
        time.sleep(10)
        url = "https://www.huxiu.com" + url
        print("-----------------------解析新闻 " + url)
        the_page = urllib.request.urlopen(url)
        # 需求：解析的字段有哪些？ 是根据实际的需求来的
        # 标题，内容，收藏，评论，点赞，时间
        page_soup = BeautifulSoup(the_page)
        # select 返回的是list
        # 获取标题
        title = page_soup.select(".t-h1")[0].string
        # 获取时间
        time = page_soup.select(".article-time")[0].string
        # 获取收藏
        share = page_soup.select(".article-share")[0].string
        # 获取评论
        pl = page_soup.select(".article-pl")[0].string
        # 获取点赞
        num = page_soup.select(".num")[0].string
        # 获取文章的内容
        # 本案中国只获取文本信息
        content_value = ""
        content = page_soup.select(".article-content-wrap")
        p_list = content[0].select("p")
        for p in p_list:
            # 过滤掉不需要 作者 出品 设计等信息
            span_list = p.select("span[class=text-remarks]")
            if len(span_list) > 0:
                continue
            # 获取正文的内容
            p_value = p.string
            # 如果是空 或者 空字符串 就跳过
            if p_value == None or p_value == " ":
                continue
            content_value = content_value + p.string + "\n"

        #`url`, `title`, `share`, `zan`, `pl`, `time`, `content`
        article_list.append((url, title, share, num, pl,time,content_value))
    return article_list

def save_article_info(article_list):
    print(article_list)
    # 保存数据到mysql
    # MySQLdb的类库导入
    # 建立数据库_表结构
    # UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-1: ordinal not in range(256)
    db = MySQLdb.connect("localhost", "root", "root", "article", charset="utf8")
    cursor = db.cursor()
    insert_sql = "INSERT INTO `article`.`python_huxiu_article` ( `url`, `title`, `share`, `zan`, `pl`, `time`, `content`) VALUES( %s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(insert_sql, article_list)
    cursor.close()
    db.commit()
    db.close()


def update_headers(headers,server_id):
    # 更新headers中的cookie 中的serverid
    # 更新操作 只需要将旧的SERVERID过滤掉，保留所有的其他的cookie信息。
    cookies = headers["Cookie"]
    cookie_str = ""
    for cookie in cookies.split(";"):
        if "SERVERID" not in cookie:
            cookie_str = cookie_str + cookie +";"
    cookie_str = cookie_str + server_id
    headers["Cookie"] = cookie_str
    return headers

def get_headers(page):
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
               # "Accept-Encoding":"gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               "Connection": "keep-alive",
               "Cookie": "huxiu_analyzer_wcy_id=46ks8mvv5w5aeetr43ec; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22158ce3ac49262a-0c7039d98a4594-581c3915-1fa400-158ce3ac4935bd%22%7D; aliyungf_tc=AQAAAHahdCa76AUAU3Awtv5W62x+1QSC; PHPSESSID=aaujd29e9ajgb7nt569npmdcn4; _ga=GA1.2.1177189611.1480928707; _gat=1; Hm_lvt_324368ef52596457d064ca5db8c6618e=1482200680,1482202286,1482724863,1482751993; Hm_lpvt_324368ef52596457d064ca5db8c6618e=1482755006; screen=%7B%22w%22%3A1920%2C%22h%22%3A1080%2C%22d%22%3A1%7D; SERVERID=03a07aad3597ca2bb83bc3f5ca3decf7|1482755272|1482751991",
               "Host": "www.huxiu.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
               "Content-Length": "80",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Origin": "https://www.huxiu.com",
               "Referer": "https://www.huxiu.com/",  # 一般可以通过referer来做盗链
               "X-Requested-With": "XMLHttpRequest"
               }
    if page >=10:
        headers["Content-Length"] = "81"
    if page >=100:
        headers["Content-Length"] = "82"
    return headers


def do_paging(last_dateline,server_id):
    page = 1  # 相当于是首页
    while page < 1071:
        page += 1
        url = "https://www.huxiu.com/v2_action/article_list"
        data = {"huxiu_hash_code": "383d9100c58b3bcb6e8071e6ee0ba62d", "page": page, "last_dateline": last_dateline}
        z_data = urllib.parse.urlencode(data)
        headers = get_headers(page) #accept-encoding    去掉该参数，否则报错，见下文
        req = urllib.request.Request(url=url, data=z_data.encode("utf-8"), headers=update_headers(headers, server_id))
        resp = urllib.request.urlopen(req)

        # 打印每次请求的参数
        print(url)
        print(data)
        # print(url + "?huxiu_hash_code=" + data.get("huxiu_hash_code")+"&page=" + data.get("page")+"&last_dateline="+ data.get("last_dateline"))
        # 打印每次的请求头
        print(update_headers(headers, server_id))

        server_id = get_server_id(resp.getheaders())
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
        # 如果出现这个问题，请检查header头中的accept-encoding参数是否设置了，如果设置了请去掉。否则会报错
        # 在本例中报错的原因是，返回的header中会指定encoding-content=gzip，那么需要单独实现解析gzip的代码
        json_str = resp.read().decode('utf-8')
        # 解析json串
        page_content = json.loads(json_str)
        data = page_content.get("data")
        print(data)
        last_dateline = page_content.get("last_dateline")
        print(last_dateline)
        # 从 data中解析每个新闻的url
        url_set = get_article_urls(BeautifulSoup(data))
        article_list = parse_article(url_set)
        save_article_info(article_list)

if __name__ == '__main__':
    print("-----------------------启动爬虫.....")
    #解析首页，得到一个新闻列表，就是url_set
    #还需要得到一个 last_dateline
    server_id,last_dateline, url_set = parse_index_page()
    #两个事情：分页请求、解析url_set  开多线程去处理是最好的
    #本文中先做第一个事情：解析urlset，然后保存数据库
    #save_article_info(parse_article(url_set))
    do_paging(last_dateline,server_id)
    print("-----------------------停止爬虫.....")
    
    
    
    
    
    
    
    
    