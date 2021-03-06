#!/usr/bin/env python
# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP服务
mail_host = 'smtp.yeah.net'
mail_user = 'shanno'
mail_pass = 'jycy728' # 客户端授权码，不是密码

sender = 'shanno@yeah.net'
receivers = ['277579830@qq.com']

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header('菜鸟教程', 'utf-8')
message['To'] = Header('测试', 'utf-8')

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

def main():
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print '邮件发送成功'
    except smtplib.SMTPException as e:
        print str(e)
        print 'Error: 无法发送邮件'

if __name__ == '__main__':
    main()
