#-*-coding:utf-8 -*-

if __name__ == "__main__":
    import import_paths
    
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from concurrent.futures import ThreadPoolExecutor
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPError

import os.path
import time
from threading import RLock
import tornadoredis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json

from controllers import login_handler, main_handler
from config.settings import *
from config import common_define
from controllers import error_code
from controllers.stub__handler import *

class HybhServerApp(tornado.web.Application):

    
    def __init__(self):
        
        handlers = [                    
                    (r'/oss/?', main_handler.MainHandler),
                    (r'/oss/login', login_handler.LoginHandler),
                    (r'/oss/logout', login_handler.LogoutHandler),                    
                    ]
        
        settings = dict(
                    static_path = os.path.join(os.path.dirname(__file__), "static"),
                    template_path = os.path.join(os.path.dirname(__file__), "templates"),
                    debug = True,
                    cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
                    login_url = "/oss/login",
                   )
        
        tornado.web.Application.__init__(self, handlers, **settings)
        
        self.__mutex = RLock()
        
        #用于执行同步操作
        self.thread_pool = ThreadPoolExecutor(10)
            
        self.reset_link()
    
        self.static_export_path = os.path.join(os.path.dirname(__file__), "static/export")
        
        self.static_import_path = os.path.join(os.path.dirname(__file__), "static/import")
    
    #重置连接    
    def reset_link(self):
        with self.__mutex:
            #首先调用获取xmpp的服务器地址
            '''
            if tornado.ioloop.IOLoop.instance()._running:
                cry_times = 3
                sleep_time = 3
            else:
                cry_times = 10
                sleep_time = 10
                
            for i in xrange(cry_times):
                result = self.__get_server_info()
                if result.has_key('xmpp') is not True:
                    time.sleep(sleep_time)
                else:
                    self.xmpp_server = result['xmpp']
                    self.sip_server = result['sip']
                    break
            else:
                logging.error('get_asim_server exception, raise exception exit')
                if tornado.ioloop.IOLoop.instance()._running is not True:
                    #如果IOLoop还没有启动，说明在APP启动阶段，通过抛出异常退出            
                    raise Exception('get_asim_server exception, raise exception exit')
                else:
                    #退出APP
                    tornado.ioloop.IOLoop.instance().stop()
            '''
            
            #redis 在asim本地
            self.__redis_connection_pool = tornadoredis.ConnectionPool(max_connections=50,
                                                                       wait_for_available=True)
            
            '''
            #改用postgresql
            if common_define.ITF_DEBUG:
                self.engine = create_engine('postgresql://postgres:viewadmin2014@%s/openfire'%self.xmpp_server['ip'], echo=True)
            else:
                self.engine = create_engine('postgresql://postgres:viewadmin2014@%s/openfire'%self.xmpp_server['ip'], echo=False)
                
            self.Session = sessionmaker()
            self.Session.configure(bind=self.engine)
            '''
        
    
    #需要获取xmpp服务器的地址，使用内网地址
    def __get_server_info(self):
        url = 'http://%s:%s/server/get_inner_server'%(common_define.ASIM_DISCOVERY_SERVER, common_define.ASIM_DISCOVERY_SERVER_PORT)
        http_client = HTTPClient()
        
        result = {}        
        try:
            response = http_client.fetch(url)
        except Exception,e:
            logging.error('get_asim_server exception: %s'%e)
            return result
        
        if response.code!=200:
            logging.error('get_asim_server exception: http code %s : %s'%(response.code, response.reason))
        else:
            pass
        
        try:
            result = json.loads(response.body, encoding='utf-8')
        except:
            logging.error('get_asim_server exception: response.body %s'%(response.body))
        
        return result
        
            
        
    #每次都是获取一个新连接，必须释放，否则会用完。
    def get_redis_client(self):
        client = tornadoredis.Client(connection_pool=self.__redis_connection_pool)
        return client
    
    def get_db_session(self):
        return self.Session()
    
    def get_thread_pool(self):
        return self.thread_pool
    
    def get_static_export_path(self):
        return self.static_export_path
    
    def get_static_import_path(self):
        return self.static_import_path

if __name__ == "__main__":
    
    tornado.options.parse_command_line()
    
    application = HybhServerApp()

    application.listen(options.port) 
    
    tornado.ioloop.IOLoop.instance().start()
    
    
    