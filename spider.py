#-*- codeing = utf-8 -*-
#@Time:2022/2/26 9:12
#@Author:张佳源
#@File:spider.py
#@Sofeware:PyCharm

from bs4 import BeautifulSoup  #网页解析
import re   #正则表达式
import xlwt  #进行excel操作
import sqlite3  #进行SQLite数据库操作
import requests

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    #savepath = ".\\豆瓣电影Top250.xls"
    dbpath = "movie.db"
    #3.保存数据
    #saveData(datalist,savepath)
    saveData2DB(datalist,dbpath)

    #askURL("https://movie.douban.com/top250?start=")

#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')     #创建正则表达式对象，表示规则(字符串的模式)
#影片图片
findImage = re.compile(r'<img.*src="(.*?)"',re.S)  #re.S 让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):  #调用获取页面信息的函数
        url = baseurl + str(i*25)
        html = askURL(url)  #保存获取到的网页源码

        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):  #查找符合要求的字符串，形成列表
            #print(item)  #测试，查看电影item全部信息
            data = []  #保存一部电影的所有信息
            item = str(item)

            link = re.findall(findLink,item)[0]    #re库通过正则表达式查找指定的字符串
            data.append(link)    #添加链接

            imgSrc = re.findall(findImage,item)[0]
            data.append(imgSrc)  #添加图片

            titles = re.findall(findTitle,item)  #片名可能只有一个中文名，没有外国名
            if(len(titles) == 2):
                ctitle = titles[0]    #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","") #去掉无关的符号
                data.append(otitle)   #添加外国名
            else:
                data.append(titles[0])
                data.append(' ') #外国名字留空

            rating = re.findall(findRating,item)[0]
            data.append(rating)    #添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)   #添加评价人数

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")   #去掉句号
                data.append(inq)            #添加概述
            else:
                data.append(" ")        #留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)     #去掉<br/>
            bd = re.sub('/'," ",bd)         #替换/
            data.append(bd.strip())         #去掉前后的空格

            datalist.append(data)       #把处理好的一部电影信息放入datalist
    #print(datalist)
    return datalist

#得到指定一个URL的网页内容
def askURL(url):
        head = {  #模拟浏览器头部信息，向豆瓣服务器发送消息
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            #"Cokkie":'ll="118278"; bid=KJ1h0_ZMGGc; __utmv=30149280.17182; __yadk_uid=Z4BWa0K08KARpiGHnEH6S0M4v0GSLVNY; _vwo_uuid_v2=D6A37974181BBB6C1A579FF178AABE49B|107100c2de9ae7b1034e31a3d139756b; douban-fav-remind=1; _ga=GA1.2.305775208.1621743083; __utma=223695111.1084973561.1621763457.1626182257.1626652494.10; _pk_id.100001.4cf6=8322e8cd74e0d62b.1621763457.11.1626652502.1626182799.; __utma=30149280.305775208.1621743083.1626652470.1627016039.17; __gads=ID=de2779e1a7400887:T=1626652494:S=ALNI_MbJVld4bhIU4G3f2YEzrOSEaP6mdQ; push_doumail_num=0; push_noty_num=0; dbcl2="171825888:PnuDqkyb5dU"; ck=NCUL'
        }
        req = requests.get(url,headers=head)
        html = ""
        try:
            html = req.text
            #print(html)
        except requests.exceptions as e:
            if hasattr(e,"code"):
                print(e.code)
            if hasattr(e,"reason"):
                print(e.reason)

        return html



#保存数据
def saveData(datalist,savepath):
    print()
    book = xlwt.Workbook(encoding="utf-8")  # 创建workbook
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)  # 创建工作表
    col = ("电影链接详情","图片链接","影片中文名","影片外文名","评分","评价数","概述","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  #数据

    book.save(savepath)

def saveData2DB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
                insert into movie250(
                info_link,pic_link,cname,ename,score,rated,introduction,info)
                values (%s)'''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()




def init_db(dbpath):
    sql = '''
        create table movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        introduction text,
        info text
        )
    ''' #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
    #init_db("movietest.db")
    print("爬取完毕")