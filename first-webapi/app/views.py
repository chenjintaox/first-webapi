'''
Created on 2016/01/21

@author: chen_jintao
'''
from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html", text = "Hello World")