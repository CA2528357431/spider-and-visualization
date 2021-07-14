from flask import Flask,render_template,request
import datetime




app = Flask(__name__)


@app.route('/test/<name>') #设置网址    # <>设置变量
def hello_world1(name):# 设置内容
    return 'hello,%s'%name

@app.route('/test/<int:id>') # int:  设置变量类型，默认str
def hello_world2(id):
    return 'hello,NO.%d'%id

@app.route('/html')
def hello_world3():
    x=datetime.datetime.now()
    quote="never say die"
    return render_template("html/myhtml.html",time=x.isoformat(),quote=quote,sharelist={"caoan":"56.0%", "oswald":"30.5%", "penguin":"13.5%"},powerlist={"caoan":"50.0%", "oswald":"35.0%", "penguin":"25.0%"})

@app.route('/login',methods=["POST"])
def hello_world4():
   if request.method=="POST":
       res=request.form
       return render_template("html/result.html",res=res)


if __name__ == '__main__':
    app.run(debug=True) #开启debug
