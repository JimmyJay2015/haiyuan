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

class ResetPwdTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):        
        cls.reqid = ''
        cls.mc = redis.Redis()        
        
        
    def setUp(self):
        self.requests_session = requests.session()
    
    #全流程
    def testResetPwdFullProcess(self):
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        resp = self.requests_session.get(url)
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , 0)
        reqid = resp_json['reqid'].encode('utf-8')
        username = 'u18019100163'
        
        params = {'reqid':reqid
                 , 'username':username
                 }
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , 0)
        
        smscode = ResetPwdTestCase.mc.get('smscode_%s'%reqid)
        
        url = 'http://127.0.0.1/app/reset_pwd_submit'        
        params = {'reqid':reqid
                 , 'smscode':smscode 
                 , 'password':'1234567890'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_SUCCESS)
        
        
        
    def testResetPwdReqGetNormal(self):
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        resp = self.requests_session.get(url)
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , 0)
        
        print str(resp_json['description'].encode('utf-8'))
        
        ResetPwdTestCase.reqid = resp_json['reqid'].encode('utf-8')        
    
    def testResetPwdReqPostErrorReqid(self):
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        params = {'reqid':'123456'
                 , 'username':'12345'
                 }
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        self.assertEquals(resp.status_code , 200)        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_REQID_ERROR)
                
        print str(resp_json['description'].encode('utf-8'))
    
    def testResetPwdReqPostErrorUsername(self):
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        params = {'reqid':ResetPwdTestCase.reqid                  
                 , 'username':'12345'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_QUERY_USER_ERROR)
                
        print str(resp_json['description'].encode('utf-8'))
        
    def testResetPwdReqPostErrorSendsms(self):
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        params = {'reqid':ResetPwdTestCase.reqid                  
                 , 'username':'u11111111'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_SMS_SEND_TASK_ERROR)
                
        print str(resp_json['description'].encode('utf-8'))
        
    def testResetPwdReqPostNormal(self):
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        params = {'reqid':ResetPwdTestCase.reqid                  
                 , 'username':'u12345678'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_SUCCESS)
                
        print str(resp_json['description'].encode('utf-8'))
    
    def testResetPwdProcessTooShortPwd(self):
        smscode = ResetPwdTestCase.mc.get('smscode_%s'%ResetPwdTestCase.reqid)
        
        url = 'http://127.0.0.1/app/reset_pwd_submit'        
        params = {'reqid':ResetPwdTestCase.reqid
                 , 'smscode':smscode 
                 , 'password':'12345'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_TOO_SHORT_PASSWORD)
                
        print str(resp_json['description'].encode('utf-8'))
    
    def testResetPwdProcessInvalidReq(self):        
        
        url = 'http://127.0.0.1/app/reset_pwd_submit'        
        params = {'reqid':'sdf'
                 , 'smscode':'smscode' 
                 , 'password':'12345678'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_INVALID_REQUEST)
                
        print str(resp_json['description'].encode('utf-8'))
        
    def testResetPwdProcessSmscodeError(self):
        url = 'http://127.0.0.1/app/reset_pwd_submit'        
        params = {'reqid': ResetPwdTestCase.reqid
                 , 'smscode':'smscode' 
                 , 'password':'12345678'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_INCORRECT_SMSCODE)
                
        print str(resp_json['description'].encode('utf-8'))
        
    def testResetPwdProcessSetPwdFailed(self):
        smscode = ResetPwdTestCase.mc.get('smscode_%s'%ResetPwdTestCase.reqid)
        url = 'http://127.0.0.1/app/reset_pwd_submit'
        
        #设置密码为12345678，会触发stub模拟接口中的错误返回        
        params = {'reqid':ResetPwdTestCase.reqid
                 , 'smscode':smscode 
                 , 'password':'12345678'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_SYSTEM_BUSY)
                
        print str(resp_json['description'].encode('utf-8'))
    
    def testResetPwdProcessNormal(self):
        smscode = ResetPwdTestCase.mc.get('smscode_%s'%ResetPwdTestCase.reqid)
        
        url = 'http://127.0.0.1/app/reset_pwd_submit'        
        params = {'reqid':ResetPwdTestCase.reqid
                 , 'smscode':smscode 
                 , 'password':'1234567890'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_SUCCESS)
                
        print str(resp_json['description'].encode('utf-8'))
        
    def testTwoManyResetReqPwd(self):
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        for i in xrange(100):
            resp = self.requests_session.get(url)
            self.assertEquals(resp.status_code , 200)        
            resp_json = resp.json()
            if resp_json['return_code']!=0:
                break
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_SYSTEM_BUSY)
                
        print str(resp_json['description'].encode('utf-8'))
    
    def testTwoManyResetPwdSms(self):
        url = 'http://127.0.0.1/reset_pwd_req'        
        resp = self.requests_session.get(url)
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , 0)
        
        
        
        url = 'http://127.0.0.1/app/reset_pwd_req'        
        params = {'reqid':resp_json['reqid'].encode('utf-8')                  
                 , 'username':'u13469437073'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
                
        for i in xrange(11):
            resp = self.requests_session.post(url, data=body, headers = header)
            self.assertEquals(resp.status_code , 200)                    
            resp_json = resp.json()
            if resp_json['return_code']!=0:
                break
            
        self.assertEquals(i, 10)
        self.assertEquals(resp_json['return_code'] , err_code_mgr.ER_RESET_SMS_TOO_MANY_REQUEST)
                
        print str(resp_json['description'].encode('utf-8'))
    
    def testWhyServletOkNotRight(self):
        url = 'http://127.0.0.1/app/reset_pwd_submit'
        reqid = '11111111'
        username = 'u13162022509'
        smscode = '1234'
        #设置到redis，以便通过检查
        ResetPwdTestCase.mc.set('failed_%s'%reqid, '0')
        ResetPwdTestCase.mc.set('smscode_%s'%reqid, smscode)
        ResetPwdTestCase.mc.set('username_%s'%reqid, username)
                
        params = {'reqid':reqid         
                ,'smscode':'1234'         
                , 'password':'11111111'
                 }
        
        body = urllib.urlencode(params)
        
        header = {                  
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  }
        
        resp = self.requests_session.post(url, data=body, headers = header)
        
        self.assertEquals(resp.status_code , 200)
        
        resp_json = resp.json()
        
        self.assertEquals(resp_json['return_code'] , 0)
                
        print str(resp_json['description'].encode('utf-8'))
   

if __name__ == "__main__":
    ResetPwdTestCase.setUpClass()
    #unittest.main()
    
    suite = unittest.TestSuite()    
    #suite.addTest(ResetPwdTestCase("testResetPwdReqGetNormal"))
    #suite.addTest(ResetPwdTestCase("testResetPwdReqPostErrorReqid"))
    #suite.addTest(ResetPwdTestCase("testResetPwdReqPostErrorUsername"))    
    
    #suite.addTest(ResetPwdTestCase("testTwoManyResetPwdSms"))
    
        
    #suite.addTest(ResetPwdTestCase("testResetPwdProcessTooShortPwd"))
    #suite.addTest(ResetPwdTestCase("testResetPwdProcessInvalidReq"))
    #suite.addTest(ResetPwdTestCase("testResetPwdProcessSmscodeError"))
    #suite.addTest(ResetPwdTestCase("testResetPwdProcessSetPwdFailed"))
    #suite.addTest(ResetPwdTestCase("testResetPwdProcessNormal"))
    
    suite.addTest(ResetPwdTestCase("testResetPwdFullProcess"))
            
    runner = unittest.TextTestRunner()
    runner.run(suite)   