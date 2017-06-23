'''
Created on 2017年6月21日

@author: iBook
'''
'''
几个要素
    内容:
        发件人,收件人,邮件名,邮件内容
    服务器:
    地址,账户,密码
'''
#使用smtplib发送邮件
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib


from_name = "weduoo"
from_mail = "619069915@qq.com"

to_name = "luqiu"
to_mail = "2074747720@qq.com"

title = "哈哈"
context = "腊八"

smtp_addr = "smtp.qq.com"
user = "619069915@qq.com"
passwd = "************"

msg = MIMEText(context,"plain",_charset = "utf-8")
msg["Subjec"] = Header(title)
msg["From"] = formataddr((from_name,from_mail),charset = "utf-8")
msg["To"] = formataddr((to_name,to_mail),charset = "utf-8")

#发送邮件
server = smtplib.SMTP(host=smtp_addr,port=25)
server.login(user=user, password=passwd)

server.sendmail(formataddr((from_name,from_mail),charset = "utf-8"),
                formataddr((to_name,to_mail),charset = "utf-8"),
                msg.as_string())
#发送完成退出
server.quit()