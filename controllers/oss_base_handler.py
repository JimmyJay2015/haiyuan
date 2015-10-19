#-*-coding:utf-8 -*-

import tornado.web

from tornado import gen
    
class OssBaseHandler(tornado.web.RequestHandler):        
    def prepare(self):
        self.redis_client = self.application.get_redis_client()
    
    def on_finish(self):
        del self.redis_client
                
    def get_current_user(self):
        return self.get_secure_cookie("user")