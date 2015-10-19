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
import hashlib


from controllers import err_code_mgr
from controllers import error_code

class CheckPwdTestCase(unittest.TestCase):
    
    def setUp(self):
        self.requests_session = requests.session()
    
    
    def testNoUserParam(self):
        url = 'http://127.0.0.1:9090/plugins/oss/checkpwd?'   
        params = {'password':'testetest'}
        url += urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
                
        resp = self.requests_session.get(url, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 3)
    
    def testUserEmptyParam(self):
        url = 'http://127.0.0.1:9090/plugins/oss/checkpwd?'   
        params = {'username':"", 'password':'testetest'}
        url += urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
                
        resp = self.requests_session.get(url, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 2)
    
    def testPwdEmptyParam(self):
        url = 'http://127.0.0.1:9090/plugins/oss/checkpwd?'   
        params = {'username':"testetest", 'password':''}
        url += urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
                
        resp = self.requests_session.get(url, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 1)
        
        
    def testUserNotExist(self):
        url = 'http://127.0.0.1:9090/plugins/oss/checkpwd?'   
        params = {'username':"testtest", 'password':'testetest'}
        url += urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
                
        resp = self.requests_session.get(url, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 5)        
    
    def testIncorrectPwd(self):
        url = 'http://127.0.0.1:9090/plugins/oss/checkpwd?'   
        params = {'username':"admin", 'password':'testetest'}
        url += urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
                
        resp = self.requests_session.get(url, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 6)
        
    
    def testSuccess(self):
        url = 'http://127.0.0.1:9090/plugins/oss/checkpwd?'
        password = hashlib.md5('111111').hexdigest()
        print password   
        params = {'username':"admin", 'password':password}
        url += urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
                
        resp = self.requests_session.get(url, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 6)
    
    
    
   

if __name__ == "__main__":    
    #unittest.main()
    
    suite = unittest.TestSuite()
    
    suite.addTest(CheckPwdTestCase("testNoUserParam"))
    suite.addTest(CheckPwdTestCase("testUserEmptyParam"))
    suite.addTest(CheckPwdTestCase("testPwdEmptyParam"))
    suite.addTest(CheckPwdTestCase("testUserNotExist"))
    suite.addTest(CheckPwdTestCase("testIncorrectPwd"))
    suite.addTest(CheckPwdTestCase("testSuccess"))
    
           
    runner = unittest.TextTestRunner()
    runner.run(suite)   