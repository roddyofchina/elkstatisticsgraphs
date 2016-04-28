#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

import smtplib
from elasticsearch import Elasticsearch
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Elkapi(object):
    def __init__(self,index):
        self.host = '10.10.10.2'
        self.port = 9200
        self.index = index


    def Connect_api(self):
        server = Elasticsearch([{'host': self.host, 'port': self.port}])
        return server

    def select_errordata(self,bodydata):
        server_con = self.Connect_api()
        elk_data = server_con.count(index=self.index,body = bodydata)
        return elk_data



class sendmailhtml(object):
    def __init__(self):
        self.HOST = "smtp.qq.com"
        self.SUBJECT = u"日志分析tomcat错误输出统计"
        self.TO = ['923401910@qq.com', 'luodi@qq.com']
        self.FROM = "admin@luodi.com"

    def emailimage(self,imgsrc,imgid):
        with open(imgsrc,'rb') as f:
            msgImage = MIMEImage(f.read())
        msgImage.add_header('Content-ID',imgid)
        return msgImage

    def emailsend(self):
        msg = MIMEMultipart('related')
        msgtext = MIMEText("""
                        <table width="400" border="0" cellspacing="0" cellpadding="4">
                            <tr bgcolor="#FFB6C1" height="20" style="font-size:14:px">
                                <td colspan=2>"tomcat错误输出统计图"<a href="http://yw.logs.simpletour.com">详细>></a></td>
                            </tr>
                            <tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
                                <td width="50%"><img src="cid:wechat"> </td>
                                <td width="50%"><img src="cid:portal"> </td>
                            </tr>
                              <tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
                                <td width="50%"><img src="cid:web"> </td>
                                <td width="50%"><img src="cid:assistant"></td>
                            </tr>

                        </table>""","html","utf-8"
                        )
        msg.attach(msgtext)
        msg.attach(self.emailimage("graph_images/protal.png", "portal"))
        msg.attach(self.emailimage("graph_images/wechat.png", "wechat"))
        msg.attach(self.emailimage("graph_images/web.png", "web"))
        msg.attach(self.emailimage("graph_images/assistant.png", "assistant"))
        msg['Subject'] = self.SUBJECT
        msg['From'] = self.FROM
        msg['To']=','.join(self.TO)

        try:
            emailserver = smtplib.SMTP()
            emailserver.connect(self.HOST, "25")
            emailserver.starttls()
            emailserver.login("luodi@qq.com", "password")
            emailserver.sendmail(self.FROM, self.TO,msg.as_string())
            emailserver.quit()
            print "send.....ok"
        except Exception,e:
            print e
            print "send.....error"

