#coding: utf-8

import json
import urllib.parse
import string
import random
import os
import socket
from redis import Redis, RedisError
from flask import Flask, Response, jsonify, request
from urllib.parse import urlparse, urlencode, quote_plus

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

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
    from urllib import request, parse
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
    
@app.route('/keyval', methods=['POST','PUT'])
def ppkey(key):
    json = JsonResponse(command='CREATE' if request.method=='POST' else 'UPDATE')

    try:
        payload = request.get_json()
        json.key = payload['key']
        json.value = payload['value']
        json.command = f"{payload['key']}/{payload['value']}"
    except:
        json.error = 'Missing or malforced JSON in client request.'
        return jsonify(json), 400

    try:
        test = redis.get(json.key)
    except:
        json.error = 'Cannot connect to redis.'
        return jsonify(json), 400

    if request.method == 'POST' and not test == None:
        json.error = "Cannot create new record: key already exists."
        return jsonify(json), 409
    elif request.method == 'PUT' and not test == None:
        json.error = "Cannot update record: key does not exist"
        return jsonify(json), 404
    else:
        if redis.set(json.key, json.value) == False:
            json.error = "There was a problem creating the value in Redis."
            return jsonify(json), 400
        else:
            json.result = True
            return jsonify(json), 200

@app.route('/keyval/<string:k>', methods=['GET','DELETE'])
def gdkey(k):
    _JSON = {
        "key": k,
        "value": None,
        "command": "{} {}".format('RETRIEVE' if request.method=='GET' else 'DELETE', k),
        "result": False,
        "error": None
    } 
    try:
        test = redis.get(k)
    except RedisError:
        _JSON['error'] = "Cannot connect to redis."
        return jsonify(_JSON), 400
    if test == None:
        _JSON['error'] = "Key does not exist"
        return jsonify(_JSON), 404
    else:
        _JSON['value'] = test.decode('unicode-escape')

    if request.method == 'GET' and not test == None:
        json.error = "Cannot retrieve record: key does not exists."
        return jsonify(_JSON), 404
    elif request.method == 'DELETE' and not test == None:
        json.error = "Cannot delete record: key does not exist"
        return jsonify(_JSON), 404
    else:
        json.result = True
        return jsonify(_JSON), 200
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
