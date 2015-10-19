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

#import memcache
import redis


from controllers import err_code_mgr
from controllers import error_code

class registerUserTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.reqid = ''
        cls.mc = redis.Redis()

    def setUp(self):
        self.requests_session = requests.session()
 
    #注册请求成功
    def testRegisterValidUser(self):
        registerUserTestCase.mc.delete("register_user_smscode_%s"%registerUserTestCase.reqid)
        registerUserTestCase.mc.delete("register_user_name_%s"%registerUserTestCase.reqid)
        registerUserTestCase.mc.delete("register_user_smscode_failed_%s"%registerUserTestCase.reqid)
        registerUserTestCase.mc.delete("register_count_%s"%registerUserTestCase.reqid)
        registerUserTestCase.mc.delete("register_reqid_access_%s"%registerUserTestCase.reqid)
        
        registerUserTestCase.reqid = ''
        
        url = 'http://127.0.0.1/app/register_user?username=u11311054513'
        resp = self.requests_session.get(url)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], 0)
        registerUserTestCase.reqid = resp_json['reqid']
    
    #验证短信验证码
    def testRegisterSmscodePassed(self):
        url = 'http://127.0.0.1/app/register_verify_smscode'
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'smscode':registerUserTestCase.mc.get('register_user_smscode_%s'%registerUserTestCase.reqid)
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_SUCCESS)
        
    #提交注册信息
    def testRegisterSubmitPass(self):
        url = 'http://127.0.0.1/app/register_user'
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'password':'aqsd123123',
                    'name':'ssssss'
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_SUCCESS)
    
    #测试1分钟处理的最大注册的get请求数量
    def testIPLimited(self):
        url = 'http://127.0.0.1/app/register_user?username=u1368171011'
        for i in xrange(100):
            resp = self.requests_session.get(url+str(i))
            self.assertEquals(resp.status_code, 200) 
            resp_json = resp.json()
            print( '第'+str(i)+'次请求:'+str(resp_json['return_code'])+str(resp_json['description'].encode('utf-8')) )
            
            
    #发起注册，用户名不合法
    def testRegisterInvalidUsername(self):
        url='http://127.0.0.1/app/register_user'
        resp=self.requests_session.get(url)
        self.assertEquals(resp.status_code,200)
        resp_json=resp.json()
        self.assertEquals(resp_json["return_code"],err_code_mgr.ER_RU_VALID_PARAMETERS)
        
        url='http://127.0.0.1/app/register_user?username='
        resp=self.requests_session.get(url)
        self.assertEquals(resp.status_code,200)
        resp_json=resp.json()
        self.assertEquals(resp_json["return_code"],err_code_mgr.ER_RU_VALID_PARAMETERS)
       
        url='http://127.0.0.1/app/register_user?username=u1511105458'
        resp=self.requests_session.get(url)
        self.assertEquals(resp.status_code,200)
        resp_json=resp.json()
        self.assertEquals(resp_json["return_code"],err_code_mgr.ER_RU_VALID_PARAMETERS)
        
    #发起注册，用户名已存在
    def testRegisterExistUser(self):
        url='http://127.0.0.1/app/register_user?username=u15111054585'
        resp=self.requests_session.get(url)
        self.assertEquals(resp.status_code,200)
        resp_json=resp.json()
        self.assertEquals(resp_json["return_code"],err_code_mgr.ER_RU_USERNAME_EXIST)
        
    #发起注册，用户名24小时内只能发起10次注册
    def testRegisterLockUsername(self):
        registerUserTestCase.mc.delete("register_count_u15111060000")
        url = 'http://127.0.0.1/app/register_user?username=u15111060000'
        for i in xrange(10):
            resp = self.requests_session.get(url)
            self.assertEquals(resp.status_code, 200)
            resp_json = resp.json()
            self.assertEquals(resp_json['return_code'], err_code_mgr.ER_SUCCESS)
        
        resp = self.requests_session.get(url)
        self.assertEquals(resp.status_code, 200) 
        resp_json = resp.json()
        
        
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_TOO_MANY_REQUEST)
        

    #验证短信验证码， 短信验证码错误
    def testRegisterSmscodeCorrectReqidErrorSmscode(self):
        self.testRegisterValidUser()
        url = 'http://127.0.0.1/app/register_verify_smscode'
        params = {
                    'reqid':registerUserTestCase.reqid,
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_INCORRECT_SMSCODE)
        
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'smscode':'123'
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json() 
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_INCORRECT_SMSCODE)
        
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'smscode':'123m'
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json() 
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_INCORRECT_SMSCODE)
        
    #验证短信验证码， reqid错误
    def testRegisterSmscodeErrorReqidCorrectSmscode(self):
        self.testRegisterValidUser()
        url = 'http://127.0.0.1/app/register_verify_smscode'
        params = {
                    'smscode':registerUserTestCase.mc.get('register_user_smscode_%s'%registerUserTestCase.reqid)
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_INVALID_REQUEST)
        
        
        params = {
                    'reqid':'42331625-d468-40ba-a206-3fd6fa7eb4322123123123',
                    'smscode':registerUserTestCase.mc.get('register_user_smscode_%s'%registerUserTestCase.reqid)
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_INVALID_REQUEST)
        
    #验证短信验证码， reqid、验证码错误
    def testRegisterSmscodeErrorReqidErrorSmscode(self):
        self.testRegisterValidUser()
        url = 'http://127.0.0.1/app/register_verify_smscode'
        params = {
                    'reqid':'42331625-d468-40ba-a206-3fd6fa7eb4322123123123',
                    'smscode':1111
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_INVALID_REQUEST)
        

    #提交注册信息   参数不正确
    def testRegisterSubmitInvalidPara(self):
        self.testRegisterValidUser()
        self.testRegisterSmscodePassed()
        
        url = 'http://127.0.0.1/app/register_user'
        params = {
                    'reqid':registerUserTestCase.reqid
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_VALID_PARAMETERS)
        
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'password':'aqs121233',
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_VALID_PARAMETERS)
        
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'password':'aqs121233',
                    'name':''
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_VALID_PARAMETERS)
        
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'name':'ssssss'
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_VALID_PARAMETERS)
        
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'password':'',
                    'name':'ssssss'
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_RU_VALID_PARAMETERS)
        
        
        params = {
                    'reqid':'42331625-d468-40ba-a206-3fd6fa7eb4322123123123',
                    'password':'aqs123123',
                    'name':'ssssss'
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_INVALID_REQUEST)
        
    
    #提交注册信息   没有通过短信验证码
    def testRegisterSubmitNoAccess(self):
        self.testRegisterValidUser()
        url = 'http://127.0.0.1/app/register_user'
        params = {
                    'reqid':registerUserTestCase.reqid,
                    'password':'aqs123123',
                    'name':'ssssss'
                  }
        body = urllib.urlencode(params)
        header = {
                    'content-type':'application/x-www-form-urlencoded; charset=UTF-8'
                  }
        resp = self.requests_session.post(url,data=body, headers=header)
        self.assertEquals(resp.status_code, 200)
        resp_json = resp.json()
        self.assertEquals(resp_json['return_code'], err_code_mgr.ER_INVALID_REQUEST)
        

if __name__ == "__main__":
    registerUserTestCase.setUpClass()
    #unittest.main()
    
    suite = unittest.TestSuite()
    
    ## "\n==================注册请求接口=======================\n"
    #time.sleep(61)
    #suite.addTest(registerUserTestCase("testIPLimited"))
    ## "wait 60s and try again"
    #time.sleep(61)
    
    suite.addTest(registerUserTestCase("testRegisterInvalidUsername"))
    suite.addTest(registerUserTestCase("testRegisterLockUsername"))
    suite.addTest(registerUserTestCase("testRegisterExistUser"))
    
    # "\n=================短信验证接口=========================\n"
    suite.addTest(registerUserTestCase("testRegisterSmscodeCorrectReqidErrorSmscode"))
    suite.addTest(registerUserTestCase("testRegisterSmscodeErrorReqidCorrectSmscode"))
    suite.addTest(registerUserTestCase("testRegisterSmscodeErrorReqidErrorSmscode"))
    
    # "\n=================注册信息提交接口=========================\n"
    suite.addTest(registerUserTestCase("testRegisterSubmitInvalidPara"))
    suite.addTest(registerUserTestCase("testRegisterSubmitNoAccess"))
    
    
    # "\n==================注册请求正常流程=======================\n"
    suite.addTest(registerUserTestCase("testRegisterValidUser"))
    suite.addTest(registerUserTestCase("testRegisterSmscodePassed"))
    suite.addTest(registerUserTestCase("testRegisterSubmitPass"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)   












































