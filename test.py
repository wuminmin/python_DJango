##coding=utf-8
from authoa import login
from authoa import clearlog
from authoa import session
from alertover import SendMessage
import pymysql
from urllib import parse
import requests
import json
import re

def deprecated_async(f):
    def wrapper(*args, **kwargs):
        from threading import Thread
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

headers_base = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN;q=0.8',
        'Content-Type':'text/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
addlist=[]
session.keep_alive = False
headers = headers_base
conn=pymysql.connect(host='localhost',user='root',passwd='19890118Wsq123',db='wordpress',use_unicode=True, charset='utf8')
cursor=conn.cursor()
log=''
typecode={'0':'站址','1':'铁塔','2':'机房','3':'配套','4':'场地费','5':'市电引入','6':'维护费'}
def getaddlist():
        try:
                #cursor.execute('SELECT DISTINCT(`站址编码`) FROM crm WHERE `地市`!="池州市" AND `站址编码`<>"" AND DATEDIFF(`起租时间`,"20190401")>=0')

                cursor.execute('SELECT DISTINCT(`站址编码`) FROM crm WHERE `地市`!="池州市" AND `站址编码`<>""')
                results=cursor.fetchall()
                print(len(results))
                return results
        except Exception as err:
                print('err')

def getdiscount(add):
        try:
                url = "http://crm.chinatowercom.cn:36080/default/cn.chinatowercom.crm.sale.site.GetNewSiteInfo.getSiteCommonInfo.biz.ext"
                headers['Referer']='http://crm.chinatowercom.cn:36080/default/sale/queryRequest/cn.chinatowercom.crm.sale.site.getSiteInfo.flow?siteId=%27' + add +'%27'
                postdata='{"siteId":"' + add + '"}'
                r = session.post(url,data=postdata, headers = headers)
                content = r.content.decode('utf-8')
                j1=json.loads(content)
                k2=j1['resultData']['requestList']
                dic={}
                k3=json.loads(k2)
                for i in range(len(k3)):
                        dic[k3[i]['REQUEST_ID']]=k3[i]['REQUEST_STATUSNAME']
                #print(dic)
                j2=j1['resultData']['discount']
                j3=json.loads(j2)
                dfun=[]
                for i in range(len(j3)):
                        res=[j3[i]['REQUEST_ID']+'-'+j3[i]['ACTIVE_TIME']+'-'+typecode[j3[i]['TYPECODE']],add,j3[i]['SITE_NAME'],j3[i]['REQUEST_ID'],j3[i]['CUST_COMPANY'],dic[j3[i]['REQUEST_ID']],typecode[j3[i]['TYPECODE']],j3[i]['DISCOUNT'],j3[i]['ACTIVE_TIME'],j3[i]['INACTIVE_TIME']]
                        #print(res)
                        dfun.append(res)
                val='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'
                #print(dfun)
                cursor.executemany('replace into crmdiscount values('+val+');' ,dfun)
                conn.commit()
                ok='OK'
                return ok
        except Exception as err:
                print(err)
addlist=getaddlist()
log=login('crm')

for i in range(3):
        if log.find('错误')==-1:
                break
        else:
                clearlog()
                log=login('crm')
print(log)

@deprecated_async
def my_work(i):
    retry = 5
    res = getdiscount(str(addlist[i][0]))
    while res != 'OK':
        retry = retry - 1
        if retry == 0:
            break
        res = getdiscount(str(addlist[i][0]))
        print('第' + str(i) + '个站址' + addlist[i][0] + '重试第' + str(5 - retry))
    print('第' + str(i) + '个站址' + addlist[i][0] + '下载完毕')

for i in range(len(addlist)):
    my_work(i)
        # retry = 5
        # res = getdiscount(str(addlist[i][0]))
        # while res!='OK':
        #         retry=retry-1
        #         if retry==0:
        #                 break
        #         res = getdiscount(str(addlist[i][0]))
        #         print('第'+str(i)+'个站址'+addlist[i][0]+'重试第'+str(5-retry))
        # print('第'+str(i)+'个站址'+addlist[i][0]+'下载完毕')

