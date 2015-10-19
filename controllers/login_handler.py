#-*-coding:utf-8 -*-

import urllib
import logging
import json

import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from config import common_define
from oss_base_handler import OssBaseHandler
import err_code_mgr


class LoginHandler(OssBaseHandler):
    
    def get(self):
        self.render('login.html')
        
    @gen.coroutine
    def post(self):
        username = str(self.get_argument("username", default = ""))
        password = str(self.get_argument("password", default = ""))
        
        #默认是/oss
        next = str(self.get_argument("next", default = "/oss"))
        
        result = {'return_code':0, 'description':"success"}
        
        #用户名不能为空
        if len(username)==0:
            result['return_code'] = err_code_mgr.ER_EMPTY_USERNAME
            result['description'] = err_code_mgr.get_error_msg(err_code_mgr.ER_EMPTY_USERNAME)
            self.write(result)
            
            client_ip = self.request.headers['X-Real-Ip']
            logging.error('%s : from this ip %s'%(result['description'], client_ip))
            
            return
        
        #密码不能为空
        if len(password)==0:
            result['return_code'] = err_code_mgr.ER_EMPTY_PASSWORD
            result['description'] = err_code_mgr.get_error_msg(err_code_mgr.ER_EMPTY_PASSWORD)
            self.write(result)
            
            client_ip = self.request.headers['X-Real-Ip']
            logging.error('%s : from this ip %s'%(result['description'], client_ip))
            
            return
        
        failed_count = yield tornado.gen.Task(self.redis_client.get, 'failed_login_%s'%username)
        MAX_TRY = 10
        LIMIT_TIME = 10
        if failed_count is not None:
            if int(failed_count)>=MAX_TRY:
                result['return_code'] = err_code_mgr.ER_TOO_MANY_LOGIN_FAILED
                result['description'] = err_code_mgr.get_error_msg(err_code_mgr.ER_TOO_MANY_LOGIN_FAILED)
                self.write(result)
            
                client_ip = self.request.headers['X-Real-Ip']
                logging.error('%s : from this ip %s'%(result['description'], client_ip))
            
                return            
        else:
            pipe = self.redis_client.pipeline()
            pipe.set('failed_login_%s'%username, '0')
            pipe.expire('failed_login_%s'%username, LIMIT_TIME)
            yield gen.Task(pipe.execute)
            
        
        
        if username=='admin' and password =='admin':
            #有效期为session，浏览器关闭以后失效。
            self.set_secure_cookie("user", username, None)
        else:
            yield tornado.gen.Task(self.redis_client.incr, 'failed_login_%s'%username)
            
        
        self.write(result)
        
    def write_error(self, status_code, **kwargs):
        logging.error('login exception %s '%status_code)
        super().write_error( status_code, **kwargs)
        
        #重新获取link
        self.application.reset_link()

class LogoutHandler(OssBaseHandler):
    
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.clear_cookie("user")
        self.redirect("/oss")
        
        
                
        