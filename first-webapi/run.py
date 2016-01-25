'''
Created on 2016/01/21

@author: chen_jintao
'''
from app import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)