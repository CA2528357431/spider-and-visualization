import sqlite3
import urllib
import requests
from bs4 import BeautifulSoup
import re


import xlwt


import sqlite3


find_web = re.compile(r'<a href="(.*)">')
find_name = re.compile(r'<span class="title">(.*)</span>')
find_score = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
find_num = re.compile(r'<span>(.*)人评价</span>')
find_nameh = re.compile(r'<span class="other"> / (.*)</span>')
find_namef = re.compile(r'<span class="title"> / (.*)</span>')
find_quote = re.compile(r'<span class="inq">(.*)</span>')
find_detail = re.compile(r'''<p class="">
                            (.*)
                        </p>''', re.S)




url = "https://movie.douban.com/top250?start="


def main():
    list = getdata(url)
    for x in list:
        print(x)
        print("\n\n\n")
    #savedata_excel(list)
    savedata_sql(list)

def getdata(url):
    list = []
    for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):

        url_r = url + str(i * 25)
        x = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
        web = urllib.request.Request(url_r, headers=x)
        web_in = urllib.request.urlopen(web)
        html = web_in.read().decode("utf8")
        print(html)
        soup = BeautifulSoup(html, "html.parser")

        for x in soup.find_all("div", class_="item"):

            dic = {}
            string = str(x)

            empt=[]

            empt.append(find_web.findall(string))
            empt.append(find_name.findall(string))
            empt.append(find_namef.findall(string))
            empt.append(find_nameh.findall(string))
            empt.append(find_quote.findall(string))
            empt.append(find_num.findall(string))
            empt.append(find_score.findall(string))
            empt.append(find_detail.findall(string))


            for r in empt:
                if len(r) == 0:
                    r.append("")

            dic["web"] =empt[0][0]
            dic["name"] =empt[1][0]
            dic["namef"] =empt[2][0]
            dic["nameh"] =empt[3][0]
            dic["quote"] =empt[4][0]
            dic["num"] =empt[5][0]
            dic["score"] =empt[6][0]

            dic["stuff"] = empt[7][0].split("\n")[0].strip()
            dic["detail"] = empt[7][0].split("\n")[1].strip()

            dic["stuff"] = dic["stuff"].replace("...<br/>", " ")
            dic["stuff"] = dic["stuff"].replace("\xa0"," ")

            dic["detail"] = dic["detail"].replace("\xa0", " ")

            list.append(dic)
    return list


def savedata_excel(list):
    excel=xlwt.Workbook(encoding="utf8")
    sheet=excel.add_sheet("movie data")
    sheet.write(0, 0, "id")
    sheet.write(0, 1, "name")
    sheet.write(0, 2, "name_hk/tw")
    sheet.write(0, 3, "name_foreign")
    sheet.write(0, 4, "detail")
    sheet.write(0, 5, "stuff")
    sheet.write(0, 6, "score")
    sheet.write(0, 7, "quote")
    sheet.write(0, 8, "web")
    i=1
    for x in list:
        sheet.write(i,0,i)
        sheet.write(i, 1, x["name"])
        sheet.write(i, 2, x["nameh"])
        sheet.write(i, 3, x["namef"])
        sheet.write(i, 4, x["detail"])
        sheet.write(i, 5, x["stuff"])
        sen=x["num"]+"人评价，平均分为"+x["score"]+"/10"
        sheet.write(i, 6, sen)
        sheet.write(i, 7, x["quote"])
        sheet.write(i, 8, x["web"])
        i+=1

    excel.save("data.xls")


def savedata_sql(list):
    conn=sqlite3.connect("data.db")#建立数据库   下面的create是建表
    c=conn.cursor()

    sql='''
    CREATE TABLE IF NOT EXISTS data (id INTEGER,name TEXT,nameh TEXT,namef TEXT,detail TEXT,stuff TEXT,num TEXT,score TEXT,quote TEXT,web TEXT)
    '''

    c.execute(sql)
    i=1
    for x in list:
        sqlx='''
        INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?)
        '''
        p=(i,x["name"],x["nameh"],x["namef"],x["detail"],x["stuff"],x["num"],x["score"],x["quote"],x["web"])
        c.execute(str(sqlx),p)
        i+=1


    conn.commit()
    conn.close()
main()