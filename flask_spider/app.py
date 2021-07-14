from flask import Flask,render_template
import sqlite3


app = Flask(__name__)


@app.route('/html')
def hello_world():
    return render_template("index.html")
@app.route('/Movie_List',methods=["POST","GET"])
def MOVIE_LIST():
    con=sqlite3.connect("data.db")
    c=con.cursor()
    sql="select id,name,nameh,namef from data"
    data=c.execute(sql)

    return render_template("MOVIE_LIST.html",data=data)
@app.route('/Score_And_Response',methods=["POST","GET"])
def SCORE_AND_RESPONSE():
    con = sqlite3.connect("data.db")
    c = con.cursor()
    sql = "select id,name,num,score,quote from data"
    data = c.execute(sql)

    return render_template("SCORE_AND_RESPONSE.html",data=data)
@app.route('/Stuff_And_Detail',methods=["POST","GET"])
def STUFF_AND_DETAIL():
    con = sqlite3.connect("data.db")
    c = con.cursor()
    sql = "select id,name,detail,stuff from data"
    data = c.execute(sql)

    return render_template("STUFF_AND_DETAIL.html",data=data)
@app.route('/Movie_Source',methods=["POST","GET"])
def MOVIE_SOURCE():
    con = sqlite3.connect("data.db")
    c = con.cursor()
    sql = "select id,name,web from data"
    data = c.execute(sql)

    return render_template("MOVIE_SOURCE.html",data=data)
@app.route('/Wordcloud',methods=["POST","GET"])
def WORDCLOUD():
    con = sqlite3.connect("data.db")
    c = con.cursor()
    c.execute("select score,num from data")
    list=c.fetchall()
    data=[0,0,0,0,0]
    for x in list:
        if float(x[0])>=9.5:
            data[0] += float(x[1])
        elif float(x[0])>=9.2:
            data[1] += float(x[1])
        elif float(x[0]) >= 8.9:
            data[2] += float(x[1])
        elif float(x[0]) >= 8.6:
            data[3] += float(x[1])
        else:
            data[4] += float(x[1])



    return render_template("ECHART.html",data=data)


if __name__ == '__main__':
    app.run(debug=True)
