#-*-coding:utf-8 -*-

import hashlib

ITF_DEBUG = True

ASIM_DISCOVERY_SERVER_PORT = 20149


QUERY_USER_EXIST_URL = 'http://%s:9090/plugins/oss/userexist?'
RESET_USER_PWD_URL = 'http://%s:9090/plugins/userService/userservice?type=update&secret=openfire&'
CHEKC_USER_PWD_URL = 'http://%s:9090/plugins/oss/checkpwd?'
QUERY_USERS_ONLINE_URL = 'http://%s:9090/plugins/oss/useronline'
REGISTER_USER_URL = 'http://%s:9090/plugins/userService/userservice?type=add&secret=openfire&'
DELETE_USER_URL = 'http://%s:9090/plugins/userService/userservice?type=delete&secret=openfire&'      
ADD_USER_URL = 'http://%s:9090/plugins/userService/userservice?type=add&secret=openfire&'      
COLLECT_LOG_URL = 'http://%s:9090/plugins/oss/collectlog?'

#discovery server默认和 app server在一起
ASIM_DISCOVERY_SERVER = '127.0.0.1'

if ITF_DEBUG:    
    SEND_SMS_URL = 'http://127.0.0.1/stub/sms?u=allenforrest&p=%s&'%(hashlib.md5('xuweinan').hexdigest())
    
else:
    SEND_SMS_URL = 'http://www.smsbao.com/sms?u=allenforrest&p=%s&'%(hashlib.md5('xuweinan').hexdigest())
      

NUM_PER_PAGE = 10
