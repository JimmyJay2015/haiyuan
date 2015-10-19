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

class OssUserOnlineTestCase(unittest.TestCase):
    
    def setUp(self):
        self.requests_session = requests.session()
        
    def testOneUserOffline(self):
        url = 'http://127.0.0.1:9090/plugins/oss/useronline'   
        params = {'usernamelist':"['u01234567890']"}
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 0)
        self.assertEquals(resp_json['result']['u01234567890'] , 'unavailable')
    
    def testOneUserOnline(self):
        url = 'http://127.0.0.1:9090/plugins/oss/useronline'   
        params = {'usernamelist':"['u13916616303']"}
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 0)
        self.assertEquals(resp_json['result']['u13916616303'] , 'available')
    
    def testOneUserNotExist(self):
        url = 'http://127.0.0.1:9090/plugins/oss/useronline'   
        params = {'usernamelist':"['testtest']"}
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 0)
        self.assertEquals(resp_json['result']['testtest'] , 'unavailable')      
    
    
    def testTwoUser(self):
        url = 'http://127.0.0.1:9090/plugins/oss/useronline'   
        params = {'usernamelist':"['u01234567890', 'u13916616303']"}
        body = urllib.urlencode(params)        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        print '0x%0X : %s \r\n'%(resp_json['return_code'], str(resp_json['description'].encode('utf-8')))
        self.assertEquals(resp_json['return_code'] , 0)
        self.assertEquals(resp_json['result']['u01234567890'] , 'unavailable')
        self.assertEquals(resp_json['result']['u13916616303'] , 'available')
   

if __name__ == "__main__":    
    #unittest.main()
    
    suite = unittest.TestSuite()
    
    suite.addTest(OssUserOnlineTestCase("testOneUserOffline"))    
    suite.addTest(OssUserOnlineTestCase("testOneUserOnline"))
    suite.addTest(OssUserOnlineTestCase("testOneUserNotExist"))
    suite.addTest(OssUserOnlineTestCase("testTwoUser"))
    
           
    runner = unittest.TextTestRunner()
    runner.run(suite)   