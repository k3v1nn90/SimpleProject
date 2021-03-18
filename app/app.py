#coding: utf-8

from flask import Flask, Response, jsonify, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/")
def login():
    return render_template('login_html')

#@app.route('/')
#@app.route('/<custom_name>')
#def hello(custom_name="World"):
#    return f"Hello, {custom_name}!"

@app.route("/md5/<string:words>")
def md5(words="World"):
    return f"Hello, {words}!"

@app.route("/factorial/<int:num>")
def factor(num,fact=1):
    for i in range(1,num+1):
        fact = fact * i
    return f"input:{num}, output:{fact}"

@app.route("/fibonacci/<int:num>")
def fibo(num):
    if num == 0:
        return f"input:0, output:0"
    elif num == 1 or num == 2:
        return f"input:{num}, output:1"
    else:
        return fibo(num-1)+fibo(num-2)

@app.route("/is-prime/<int:num>")
def prime(num):
    a = "True"
    b = "False"
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return b
        else:
            return a
    else:
        return b
    return

@app.route('/slack-alert/<string:words>')
def alert(words):    
    return ('')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
