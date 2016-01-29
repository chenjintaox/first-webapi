#coding=utf-8

'''
Created on 2016/01/21

@author: chen_jintao
'''
from app import app
from flask import render_template
from flask import jsonify
#导入SHA1
import os
from hashlib import sha1
#导入uuid4
#from uuid import uuid1

from functools import wraps
from flask.globals import request

def check_auth(username, password):
    return username == 'admin' and password == 'token'

def authenticate():
    message = {"message" : "Authenticate"}
    resp = jsonify(message)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    return resp
    
    
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:#没有请求认证
            return authenticate()
        elif not check_auth(auth.username, auth.password):#请求的认证信息不正确
            return authenticate()
        return f(*args, **kwargs)
    
    return decorated

#生成token、
def generate_tokens():
    return sha1(os.urandom(24)).hexdigest()
    #return uuid1().hex
    

@app.route('/')
def index():
    return render_template("index.html", text = "Hello World")

#获取令牌
@app.route('/tokens')
@requires_auth
def api_tokens():
    return generate_tokens()