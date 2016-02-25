#coding=utf-8

'''
Created on 2016/01/21

@author: chenjintaox
参考url：http://blog.luisrei.com/articles/flaskrest.html
'''
from app import app
from flask import render_template
from flask import json
from flask import jsonify
import logging

#导入SHA1
import os
from hashlib import sha1
#导入uuid4
#from uuid import uuid1

from functools import wraps
from flask.globals import request
from flask.helpers import url_for
from pip._vendor.html5lib.html5parser import method_decorator_metaclass
from flask.wrappers import Response

#增加log功能
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

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


###############资源（RESOURCES）###############
#获取文章列表
@app.route('/articles')
def api_articles():
    return 'List of'+url_for('api_articles')
#获取指定文章
#@app.route('/articles/<int:articleid>')
#@app.route('/articles/<float:articleid>')
#@app.route('/articles/<path:articleid>')
@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid


###############请求（REQUESTS）############### 
#GET 参数(GET /hello,/hello?name='zhangsan')
@app.route('/hello')
def api_hello():
    #log功能测试
    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('screaming bloody murder!')
    
    if 'name' in request.args:
        return 'hello ' + request.args['name']
    else:
        return 'hello chenjintaox'
#请求方式（Request Methods）：['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO:GET\n"
    elif request.method == 'POST':
        return "ECHO:POST\n"
    elif request.method == 'PATCH':
        return "ECHO:PATCH"
    elif request.method == 'PUT':
        return "ECHO:PUT"
    elif request.method == 'DELETE':
        return "ECHO:DELETE"
    
#请求 数据和头部（Request Data & Headers）
'''
传递数据，通常使用POST和PATCH，数据的格式通常包括，纯文本，JSON，XML，二进制，自定义格式；
通过request.headers（字典）,访问HTTP的头部;
通过reauest.data（字符串）,访问HTTP数据；
如果mimetype是application/json，通过request.json访问JSON数据
''' 
@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'text/plain':
        return 'Text Message: ' + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return 'Json Message: ' + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return 'Binary message written!'
    else:
        return '415 Unsupported Media Type'
    
###############回应(RESPONSES)###############
#通过flask的Response class来回应请求
@app.route('/hi', methods = ['GET'])
def api_hi():
    data = {
        'hello' : 'world',
        'nmuber' : 3,
    }
    js = json.dumps(data)
    resp = Response(js, status = 200, mimetype='application/json')
    return resp

###############(Status Codes & Errors)###############
@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status':404,
        'message':'not found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/users/<userid>', methods = ['GET'])
def api_users(userid):
    users = {'1':'john', '2':'steve', '3':'bill'}
    
    if userid in users:
        return jsonify({userid:users[userid]})
    else:
        return not_found()