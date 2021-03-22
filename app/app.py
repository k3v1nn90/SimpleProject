from flask import Flask, Response, jsonify
import urllib.parse
from urllib.parse import urlparse, urlencode, quote_plus
from urllib import request, parse
import json
import string
import random

app = Flask(__name__)

@app.route("/md5/<string:words>")
def md5(words, chars=string.ascii_letters + string.digits):
    x="{"
    y="}"
    leng = len(words)
    words = urllib.parse.quote(words)
    txt=(''.join(random.choice(chars) for x in range(leng)))
    return f"{x}\n\"input\": {words},\n\"output\": {txt}\n{y}"

@app.route("/factorial/<int:num>")
def factor(num,fact=1):
    for i in range(1,num+1):
        fact = fact * i
    return f"input: {num}, output: {fact}"

@app.route('/fibonacci/<int:val>')
def term(val):
    x="{"
    y="}"
    Out = 0
    Sequence = [0,1]
    if val > 0:
        while Out < val:
            Out = Sequence[-1] + Sequence[-2]
            if (Out < val):
                Sequence.append(Out)
        return f"{x}\n\"input\": {val},\n\"output\": {Sequence}\n{y}"
    elif val <=0:
        return f"That is not a valid number"

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
