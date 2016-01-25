#coding=utf-8

'''
Created on 2016/01/21

@author: chen_jintao
'''
from app import app
from flask_script import Server,Manager

manager = Manager(app)
manager.add_command("runserver", 
                    Server(host='0.0.0.0', port=5000, use_debugger=True))

if __name__ == '__main__':
    manager.run()