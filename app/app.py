from flask import Flask, Response, jsonify
import urllib.parse
from urllib.parse import urlparse, urlencode, quote_plus
from urllib import request, parse
import json

app = Flask(__name__)

@app.route("/md5/<string:words>")
def md5(words):
    x="{"
    y="}"
    encoded_query = urllib.parse.quote(words)
    return f"{x}\n\"input\": {words},\n\"output\": {encoded_query}\n{y}"

@app.route("/factorial/<int:num>")
def factor(num,fact=1):
    x="{"
    y="}"
    for i in range(1,num+1):
        fact = fact * i
    return f"{x}\n\"input\": {num},\n\"output\": {fact}\n{y}"

@app.route("/fibonacci/<int:num>")
def fibo(num):
    nterms = num
    n1, n2 = 0, 1
    count = 0
    if nterms < 0:
        return f"Please enter a positive integer"
    elif nterms == 1:
        return f"{n1}"
    else:
        while count < nterms:
            array = []
            nth = n1 + n2
            n1 = n2
            n2 = nth
            array.append(n1)
            count += 1
        return f"{array}"

@app.route("/is-prime/<int:num>")
def prime(num):
    x="{"
    y="}"
    a = "True"
    b = "False"
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return f"{x}\n\"input\": {num},\n\"output\": {b}\n{y}"
        else:
            return f"{x}\n\"input\": {num},\n\"output\": {a}\n{y}"
    else:
        return f"{x}\n\"input\": {num},\n\"output\": {b}\n{y}"
    return

@app.route('/slack-alert/<string:text>')
def alert(text):
    x="{"
    y="}"
    a = "True"
    b = "False"
    post = {"text": "{0}".format(text)}
    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",data=json_data.encode('ascii'),headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
        return f"{x}\n\"input\": {text},\n\"output\": {a}\n{y}"     
    except Exception as em:
        print("EXCEPTION: " + str(em))
        return f"{x}\n\"input\": {text},\n\"output\": {b}\n{y}"
    alert(f'{text}')

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
