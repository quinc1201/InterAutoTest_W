#!/usr/bin/python
# -*- coding: UTF-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# 初始化
# SMTP地址，用户名，密码，接收邮件人，邮件标题，邮件内容，邮件附件
class SendEmail:
    def __init__(self, smtp_addr, username, passwd, recv, title, content=None, file=None):
        self.smtp_addr = smtp_addr
        self.username = username
        self.password = passwd
        self.recv = recv
        self.title = title
        self.content = content
        self.file = file

    # 发送邮件的方法
    def send_email(self):
        msg = MIMEMultipart()
        # 初始化邮件信息
        msg.attach(MIMEText(self.content, _charset='utf8'))
        msg['Subject'] = self.title
        msg['From'] = self.username
        msg['To'] = self.recv
        # 附件
        # 判断是否有附件
        if self.file:
            # MIMEText读取文件
            att = MIMEText(open(self.file).read())
            # 设置内容类型
            att['Content-Type'] = 'application/octet-stream'
            # 设置附件头
            att['Content-Disposition'] = 'attachment;filename="{}"'.format(self.file)
            # 将内容添加到邮件主体中
            msg.attach(att)
        # 登录邮件服务器
        self.smtp = smtplib.SMTP(self.smtp_addr, port=25)
        self.smtp.login(self.username, self.password)
        # 发送邮件
        self.smtp.sendmail(self.username, self.recv, msg.as_string())


if __name__ == '__main__':
    from config.conf import ConfigYaml
    email_info = ConfigYaml().get_email_info()
    smtp_addr = email_info['smtpserver']
    username = email_info['username']
    password = email_info['password']
    recv = email_info['receiver']
    email = SendEmail(smtp_addr, username, password, recv, title='测试')
    email.send_email()

    # 封装公共方法
    # 应用测试用例