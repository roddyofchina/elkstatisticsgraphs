#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

import datetime,time
from elkserverapi import  Elkapi,sendmailhtml
from Graph_elk import graphserver

class Getelkdata(Elkapi):

    def time_str(self,startimes):
        strtime=str(startimes)+'00'
        strtime=strtime.replace('.','')
        return strtime

    def search_body(self,searchsql,starttime,stoptime):
        starttime=self.time_str(starttime)
        stoptime=self.time_str(stoptime)

        #接口请求字段
        searchdata = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "analyze_wildcard": "true",
                            "query": searchsql
                        }
                    },

                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "range": {
                                        "@timestamp": {
                                            "gte": starttime,
                                            "lte": stoptime,
                                            "format": "epoch_millis"
                                        }
                                    }
                                }
                            ],
                            "must_not": [
                            ]
                        }
                    }
                }
            },
        }
        errordatacount=self.select_errordata(searchdata)
        return errordatacount

    def Timeday(self,searchsql):
        days=[]
        counts=[]

        today = datetime.datetime.today()
        for tm in range(1,8):
            yesterday = today - datetime.timedelta(hours = 24*tm)

            days.append(yesterday.strftime('%Y-%m-%d'))  #拼接时间列表

            stimes = datetime.datetime(yesterday.year,yesterday.month,yesterday.day,00)  #一天的时间

            endtime = datetime.datetime(yesterday.year,yesterday.month,yesterday.day,23)

            sstime=time.mktime(stimes.timetuple())

            estime=time.mktime(endtime.timetuple())

            errordata=self.search_body(searchsql,sstime,estime)
            counts.append(errordata['count'])

        return days,counts

    def graphs(self,searchsql,program_name):

        days,counts=self.Timeday(searchsql)
        days.reverse(),counts.reverse()  #列表倒序排列，时间从前到后
        graphs=graphserver([days,counts])
        graphs.graph_Save(program_name)




wechat=Getelkdata('tomcat-log-2016-04')
wechat.graphs("Host_Name:\"微信\" AND message: *exception*",'wechat')

protal=Getelkdata('tomcat-log-2016-04')
protal.graphs("Host_Name:\"后台\" AND message: *exception*",'protal')

web=Getelkdata('tomcat-log-2016-04')
web.graphs("Host_Name:\"网站\" AND message: *exception*",'web')

assistant=Getelkdata('tomcat-log-2016-04')
assistant.graphs("Host_Name:\"助理\" AND message: *exception*",'assistant')

mails=sendmailhtml()
mails.emailsend()
