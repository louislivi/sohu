#!/usr/bin/python
#-*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib,urlparse
import json,sys,os
import re,random,time
import MySQLdb
from pyquery import PyQuery as pyq
reload(sys)
sys.setdefaultencoding('utf8')

def remove_emoji(desstr,restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
db = MySQLdb.connect("rm-wz992d32df6c8t3u5242.mysql.rds.aliyuncs.com", "maiya", "P--!jathJhk1UbE3FthiYNmOQJW+XHeX", "news", charset='utf8' )
cursor = db.cursor()

t = time.time()
json_callback = str(int(round(t * 1000)))
json_data = []
cj=cookielib.LWPCookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
url = "https://pv.sohu.com/suv/?t?=1530072830304583_375_812?r?="
req=urllib2.Request(url)
req.add_header('Referer','https://m.sohu.com/ch/28')
req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')
ret=urllib2.urlopen(req)
ret.read()

for pre_page in range(1,11):
    for channelId in [8,10,12,13,15,17,18,19,23,24,25,26,27,28,29,30,41,42,43,44,45]:
        previous_cookie = ''
        for index, scj in enumerate(cj):
            previous_cookie += scj.name + '=' + scj.value + ';'
        # print page
        # continue
        url = "http://v2.sohu.com/public-api/articleFeed?channelId="+str(channelId)+"&page="+str(pre_page)+"&size=100&callback=jQuery3310800558194836734_"+json_callback+"&_="+str(int(round(t * 1000)))
        req=urllib2.Request(url)
        req.add_header('Referer','https://m.sohu.com/ch/'+str(channelId))
        req.add_header('Cookie',previous_cookie)
        req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')
        ret=urllib2.urlopen(req)
        regex_content = re.compile(
                    '^/\*\*/jQuery3310800558194836734_'+json_callback+'\((.*?)\);$',
                    re.S)
        items = re.findall(regex_content, ret.read())
        data = json.loads(items[0])
        for item,value in enumerate(data):
            data[item]["authorPic"] = re.sub(r'^\/\/',"https://",re.sub(r'a_auto,.*?\/',"",data[item]["authorPic"]))
            data[item]["picUrl"] = re.sub(r'^\/\/',"https://",re.sub(r'a_auto,.*?\/',"",data[item]["picUrl"]))
            for key,image_url in enumerate(value["images"]):
                data[item]["images"][key] = re.sub(r'^\/\/',"https://",re.sub(r'a_auto,.*?\/',"",image_url))
            article_url = 'https://m.sohu.com/a/%d_%d' % (value["id"],value["authorId"])
            page = urllib2.urlopen(article_url)
            page_data = page.read()
            doc = pyq(page_data)
            if doc(".place_video"):
                continue
            doc("article").find(".promotion").remove()
            doc("article").find("footer").remove()
            doc("article").find(".statement").remove()
            doc("article").find(".article-footer").remove()
            doc("article").find("#artLookAll").remove()
            if doc("article").find("img"):
                for img_doc in doc("article").find("img"):
                    if doc(img_doc).attr("src"):
                        doc(img_doc).attr("src",re.sub(r'^\/\/',"https://",doc(img_doc).attr("src")))
                    if doc(img_doc).attr("data-src"):
                        doc(img_doc).attr("src",re.sub(r'^\/\/',"https://",doc(img_doc).attr("data-src")))
            data[item]["article"] = doc("article").html()
            if data[item]["article"] and json.dumps(data[item]["images"]) != "[]" and data[item]["picUrl"]:
                try:
                    sql = """INSERT INTO
                    `article` (`id`, `author_id`, `author_pic`, `author_name`, `title`, `picurl`, `images`, `public_time`, `cms_id`,`reading`, `type`, `create_time`, `update_time`)
                VALUES (%d, %d, '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, DEFAULT, DEFAULT)""" % (
                  data[item]["id"],data[item]["authorId"],data[item]["authorPic"],data[item]["authorName"],remove_emoji(data[item]["title"]),data[item]["picUrl"],json.dumps(data[item]["images"]),
                  int(str(data[item]["publicTime"])[:10]),data[item]["cmsId"],random.randint(5000,200000),channelId
                )
                    sql2 = """INSERT INTO
                `article_content` (`article_id`, `content`)
                VALUES (%d,'%s')""" % (
                  data[item]["id"],remove_emoji(data[item]["article"].encode('latin1').decode('utf8'))
                  )
                    try:
                        # 执行sql语句
                        cursor.execute(sql)
                        cursor.execute(sql2)
                        # 提交到数据库执行
                        db.commit()
                    except:
                        # Rollback in case there is any error
                        db.rollback()
                except:
                    continue

# json_data = data+json_data
db.close()
