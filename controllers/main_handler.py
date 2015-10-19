#-*-coding:utf-8 -*-

import tornado.web

from oss_base_handler import OssBaseHandler

class MainHandler(OssBaseHandler):
    
    @tornado.web.authenticated # 如果没有登陆，就自动跳转到登陆页面
    def get(self):
        self.redirect('/oss/enterprise_device/list')
