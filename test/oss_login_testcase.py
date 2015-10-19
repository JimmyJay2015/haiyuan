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


from controllers import err_code_mgr
from controllers import error_code

class OssLoginTestCase(unittest.TestCase):
    
    
        
    def setUp(self):
        self.requests_session = requests.session()
    
    def testLoginSuccess(self):
        url = 'http://127.0.0.1/oss/login'   
        params = {'username':'admin'                  
                 , 'password':'111111'
                 }
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 0)
        
    def testLoginUsernameEmpty(self):
        url = 'http://127.0.0.1/oss/login'   
        params = {'username1':'admin1'                  
                 , 'password':'111111'
                 }     
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0x : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_EMPTY_USERNAME)
    
    def testLoginPasswordEmpty(self):
        url = 'http://127.0.0.1/oss/login'   
        params = {'username':'admin1'                  
                 , 'password1':'111111'
                 }     
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0x : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_EMPTY_PASSWORD)
        
    
    def testLoginUsernameFailed(self):
        url = 'http://127.0.0.1/oss/login'   
        params = {'username':'admin1'                  
                 , 'password':'111111'
                 }     
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0x : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_NEED_ADMIN)
    
    def testLoginPasswordFailed(self):
        url = 'http://127.0.0.1/oss/login'   
        params = {'username':'admin'                  
                 , 'password':'1111'
                 }     
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0x : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_INCORRECT_PWD)
    
    def testLoginPasswordTooManyFailed(self):
        url = 'http://127.0.0.1/oss/login'   
        params = {'username':'admin'                  
                 , 'password':'1111'
                 }     
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        for i in xrange(10):        
            resp = self.requests_session.post(url, data=body, headers = header)
            self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0x : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_TOO_MANY_LOGIN_FAILED)
   

if __name__ == "__main__":    
    #unittest.main()
    
    suite = unittest.TestSuite()
    
    suite.addTest(OssLoginTestCase("testLoginUsernameEmpty"))
    suite.addTest(OssLoginTestCase("testLoginPasswordEmpty"))
    suite.addTest(OssLoginTestCase("testLoginUsernameFailed"))
    suite.addTest(OssLoginTestCase("testLoginPasswordFailed"))    
    suite.addTest(OssLoginTestCase("testLoginSuccess"))
    
    suite.addTest(OssLoginTestCase("testLoginPasswordTooManyFailed"))
    
           
    runner = unittest.TextTestRunner()
    runner.run(suite)   