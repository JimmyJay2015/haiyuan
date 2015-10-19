#-*-coding:utf-8 -*-

import logging
import tornado.web
import hashlib
import time

import err_code_mgr

from tornado import gen

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Unicode, DateTime 

#模拟查询用户是否存在，username 长度>=8 返回存在；否则，返回不存在。    
class StubUserExistHandler(tornado.web.RequestHandler):
    def get(self):
        username = str(self.get_argument("username", default = ""))
        
        result = {'return_code':0, 'description':"success"}
        
        if len(username) < 8:
            result['return_code'] = 1
            result['description'] = '测试'
        
        self.write(result)

class StubSendSmsHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        username = str(self.get_argument("u", default = ""))
        password = str(self.get_argument("p", default = ""))
        user_phone = str(self.get_argument("m", default = ""))
        content = str(self.get_argument("c", default = "").encode('utf-8'))
        
        result = '0'
        
        if username!='allenforrest':            
            result = '40'            
        if password!= hashlib.md5('xuweinan').hexdigest():            
            result = '30'                
        if user_phone=='51':            
            result = 'user phone error'        
        
        self.write(result)
                
        #把注册码放到redis中，可以查询出来
        description = "%s , %s, %s"%(time.ctime(), user_phone, content)
        pipe = self.redis_client.pipeline()
        pipe.lpush('sub_sms', description)
        pipe.expire('sub_sms', 3600)
        yield gen.Task(pipe.execute)
        
    def prepare(self):        
        self.redis_client = self.application.get_redis_client()

    def on_finish(self):
        del self.redis_client

class StubSmsQueryHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        
        len = yield gen.Task(self.redis_client.llen, 'sub_sms')
        resultlist = yield gen.Task(self.redis_client.lrange, 'sub_sms', 0, len-1)
        resultstr = ''        
        for item in resultlist:
            resultstr += '<h4>%s<h4>'%item.encode('utf-8')
        out = '<html><body>%s</body></html>'%resultstr   
        self.write(out)
        
    def prepare(self):        
        self.redis_client = self.application.get_redis_client()

    def on_finish(self):
        del self.redis_client        
        
    
class StubResetPwdHandler(tornado.web.RequestHandler):
    def get(self):
        type = str(self.get_argument("type", default = ""))
        secret = str(self.get_argument("secret", default = ""))
        username = str(self.get_argument("username", default = ""))
        password = str(self.get_argument("password", default = ""))
        
        result = '<result>%s</result>'
        
        if type!='update':            
            result = result%'type error'            
        if secret!='bigsecret':            
            result = result%'secret error'                
        if password=='12345678':            
            result = result%'password error'
        else:
            result = result%'ok'
        
        
        self.write(result)

class StubCheckPwdHandler(tornado.web.RequestHandler):
    def get(self):        
        username = str(self.get_argument("username", default = ""))
        password = str(self.get_argument("password", default = ""))
        
        result = {'return_code':0, 'description':"success"}
        
                
        
          
#模拟注册#######################################################################################
class StubRegisterUserHandler(tornado.web.RequestHandler):        
    def get(self):        
        type = str(self.get_argument("type", default = ""))
        secret = str(self.get_argument("secret", default = ""))
        username = str(self.get_argument("username", default = ""))
        password = str(self.get_argument("password", default = ""))
        name = str(self.get_argument("name", default = ""))
    
        result = '<result>%s</result>'       
        
        if type!='add':            
            result = result%'type error'
        elif secret!='bigsecret':
            result = result%'secret error' 
        elif password=="":
            result = result%'password error'
        elif username=="":
            result = result%'username error'
        elif name=="":
            result = result%'username error'
        else:
            result = result%'ok'
        
        self.write(result)      
        
#模拟删除用户
class UseDeleteHandler(tornado.web.RequestHandler):
    def get(self):
        result = {'return_code':0, 'description':"success"}
        username = str(self.get_argument("username", default = ""))
        
        logging.info("stub UseDeleteHandler username:%s"%username)
        
        if len(username) <= 0 or username[0] != 'u':
            result['return_code'] = err_code_mgr.ER_UM_INVALID_USER_NAME
            result['description'] = err_code_mgr.get_error_msg(err_code_mgr.ER_UM_INVALID_USER_NAME)
            logging.info("stub UseDeleteHandler error 1 result:%s"%str(result))
            self.write(result)
            return
        
        if username != 'u15111054555':
            result['return_code'] = err_code_mgr.ER_UM_USER_NAME_NOT_EXIST
            result['description'] = err_code_mgr.get_error_msg(err_code_mgr.ER_UM_USER_NAME_NOT_EXIST)
            logging.info("stub UseDeleteHandler error 2 result:%s"%str(result))
            self.write(result)
            return
        
        logging.info("stub UseDeleteHandler result:%s"%str(result))
        self.write(result)
        return
    
    
               
        
        
        
        
        
        
        
        
        
        
        