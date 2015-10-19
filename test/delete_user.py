#coding=utf-8

if __name__ == "__main__":
    import import_paths
        
import unittest
import threading
import time
import copy

import requests
import urllib
import mimetools

import redis

from controllers import err_code_mgr
from controllers import error_code

class DeleteUserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):        
        cls.reqid = ''
        cls.mc = redis.Redis()        
        
        
    def setUp(self):
        self.requests_session = requests.session()
        
        
    def testDeleteOK(self):
        url = "http://127.0.0.1/oss/user_management/delete"
        
        params = {'username':'u15111054555'
                 }
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        resp_json = resp.json()
        print ( ' testDeleteOK resp_json ' + str(resp_json) )
        self.assertEquals(resp_json['return_code'] , 0)
    
    def testDeleteFailed(self):
        #没有用户名
        url = "http://127.0.0.1/oss/user_management/delete"
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url, headers = header)
        self.assertEquals(resp.status_code , 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_UM_INVALID_USER_NAME)
        
        
        #用户名不合法
        url = "http://127.0.0.1/oss/user_management/delete"
        params = {
                  'username':'123123'
                 }
        body = urllib.urlencode(params)
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_UM_INVALID_USER_NAME)
        
        #用户不存在
        url = "http://127.0.0.1/oss/user_management/delete"
        params = {'username':'u1511105499asd'
                 }
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_UM_USER_NAME_NOT_EXIST)
    
        
if __name__ == "__main__":
    DeleteUserTestCase.setUpClass()
    
    suite = unittest.TestSuite()    
    suite.addTest(DeleteUserTestCase("testDeleteOK"))
    #suite.addTest(DeleteUserTestCase("testDeleteFailed"))
            
    runner = unittest.TextTestRunner()
    runner.run(suite)   