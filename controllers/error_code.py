#-*-coding:utf-8 -*-

"""
Copyright (C), 2012-2015, 
Author: 
Version: 1.0
Date: 2012-11-30
Description: 错误码定义文件
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-11-30
   Author:
   Modification:新建文件
"""

import err_code_mgr

#SERVER 命令码
ERROR_BASE = 0X10000
RESET_PWD_ERROR_BASE = ERROR_BASE

reset_pwd_error_defs = {"ER_REQID_ERROR" : (RESET_PWD_ERROR_BASE + 1
                                             , "请求ID无效"
                                             , "request id illegal")
                        , "ER_SMS_SEND_TASK_ERROR" : (RESET_PWD_ERROR_BASE + 2
                                            , "短信验证码发送失败,具体信息:%(detail_info)s"
                                            , "send sms failed, detail information: %(detail_info)s")
                        ,"ER_TOO_SHORT_PASSWORD": (RESET_PWD_ERROR_BASE+3
                                            ,"密码长度太短"
                                            ,"to short password")                            
                        ,"ER_TOO_MANY_SMSCODE_FAILED": (RESET_PWD_ERROR_BASE+4
                                            ,"短信验证码验证失败次数过多，请重新申请短信验证码后操作"
                                            ,"too many sms code failed")
                        ,"ER_INCORRECT_SMSCODE": (RESET_PWD_ERROR_BASE+5
                                            ,"短信验证码不正确"
                                            ,"sms code incorrect")                        
                        ,"ER_QUERY_USER_ERROR": (RESET_PWD_ERROR_BASE+6
                                            ,"查询用户失败,具体信息:%(detail_info)s"
                                            ,"query user failed, detail information: %(detail_info)s")
                        ,"ER_RESET_SMS_TOO_MANY_REQUEST": (RESET_PWD_ERROR_BASE+7          
                                            ,"1天内最多10次重置密码请求"
                                            ,"too many request")
                
             }
err_code_mgr.regist_errors(reset_pwd_error_defs)


LOGIN_ERROR_BASE = ERROR_BASE + 0X10
login_error_defs = {"ER_EMPTY_USERNAME" : (LOGIN_ERROR_BASE + 0
                                             , "用户名不能为空"
                                             , "empty username")
                        , "ER_EMPTY_PASSWORD" : (LOGIN_ERROR_BASE + 1
                                             , "密码不能为空"
                                             , "empty password")
                        , "ER_TOO_MANY_LOGIN_FAILED" : (LOGIN_ERROR_BASE + 2
                                             , "登录失败次数过多，禁止登录10分钟"
                                             , "too many login failed")
                        , "ER_NEED_ADMIN" : (LOGIN_ERROR_BASE + 3
                                             , "需要管理员帐号"
                                             , "admin user is needed")                        
                        , "ER_INCORRECT_PWD" : (LOGIN_ERROR_BASE + 4
                                             , "密码错误"
                                             , "incorrect password")
                        ,"ER_CHECK_PWD_OTHER_ERROR": (LOGIN_ERROR_BASE+5
                                            ,"检查管理员密码失败,具体信息:%(detail_info)s"
                                            ,"check admin password failed, detail information: %(detail_info)s")                        
                                        
             }
err_code_mgr.regist_errors(login_error_defs)


ENTERPRISE_DEVICE_ERROR_BASE = ERROR_BASE + 0X20
enterprise_device_error_defs = {"ER_DEVICE_NOT_FOUND" : (ENTERPRISE_DEVICE_ERROR_BASE + 0
                                             , "设备不存在"
                                             , "device not exist")
                        , "ER_ADD_DEVICE_EXCEPTION" : (ENTERPRISE_DEVICE_ERROR_BASE + 1
                                             , "增加设备信息出现异常，具体信息：%(detail_info)s"
                                             , "add device exception，detail information: %(detail_info)s")
                        , "ER_DELETE_DEVICE_EXCEPTION" : (ENTERPRISE_DEVICE_ERROR_BASE + 2
                                             , "删除设备信息出现异常，具体信息：%(detail_info)s"
                                             , "delete device exception，detail information: %(detail_info)s")
                        , "ER_MOD_DEVICE_EXCEPTION" : (ENTERPRISE_DEVICE_ERROR_BASE + 3
                                             , "更新设备信息出现异常，具体信息：%(detail_info)s"
                                             , "mod device exception，detail information: %(detail_info)s")
                        
                                        
             }
err_code_mgr.regist_errors(enterprise_device_error_defs)

#注册新用户错误信息
REGISTER_USER_ERROR_BASE = ERROR_BASE+0x10000
register_user_error_defs = {"ER_RU_USERNAME_EXIST" : (REGISTER_USER_ERROR_BASE + 0
                                             , "用户已注册"
                                             , "user has already Registered")
                            , "ER_RU_SMS_SEND_TASK_ERROR" : (RESET_PWD_ERROR_BASE + 1   
                                            , "短信验证码发送失败,具体信息:%(detail_info)s"
                                            , "send sms failed, detail information: %(detail_info)s")
                            ,"ER_RU_QUERY_ERROR" : (REGISTER_USER_ERROR_BASE + 2   
                                             , "查询用户失败,具体信息:%(detail_info)s"
                                             , "query user failed, detail information: %(detail_info)s")
                            , "ER_RU_SMS_SEND_TASK_ERROR" : (REGISTER_USER_ERROR_BASE + 3   
                                            , "短信验证码发送失败,具体信息:%(detail_info)s"
                                            , "send sms failed, detail information: %(detail_info)s")
                            , "ER_RU_VALID_PARAMETERS" : (REGISTER_USER_ERROR_BASE + 4   
                                            , "参数不合法"
                                            , "valid parameters")
                            ,"ER_RU_TOO_MANY_SMSCODE_FAILED": (REGISTER_USER_ERROR_BASE+5   
                                            ,"短信验证码验证失败次数过多，请重新申请短信验证码后操作"
                                            ,"too many sms code failed")
                            ,"ER_RU_INCORRECT_SMSCODE": (REGISTER_USER_ERROR_BASE+6   
                                            ,"短信验证码不正确"
                                            ,"sms code incorrect")
                            ,"ER_RU_NO_ACCESS": (REGISTER_USER_ERROR_BASE+7
                                            ,"此reqid没有通过短信验证"
                                            ,"reqid should get register access")
                            ,"ER_RU_TOO_MANY_REQUEST": (REGISTER_USER_ERROR_BASE+8          
                                            ,"请求注册次数过多"
                                            ,"too many request")
             }
err_code_mgr.regist_errors(register_user_error_defs)

#导入导出错误信息
IMPORT_EXPORT_ERROR_BASE = REGISTER_USER_ERROR_BASE + 0x20
import_export_error_defs = {"ER_IE_DELETE_FILE_INVALIDNAME":(IMPORT_EXPORT_ERROR_BASE + 0
                                            ,"无效的文件名"
                                            ,"invalid file name")
                            , "ER_IE_DELETE_FILE_FAILED":(IMPORT_EXPORT_ERROR_BASE + 1
                                            ,"删除失败"
                                            ,"delete file failed")
                            , "ER_IE_EXPORT_DATA_FAILED":(IMPORT_EXPORT_ERROR_BASE + 2
                                            ,"导出数据失败"
                                            ,"export data failed")
                            , "ER_IE_IMPORT_INVALID_FILE":(IMPORT_EXPORT_ERROR_BASE + 3
                                            ,"无效的导入文件"
                                            ,"invalid import file")
                            , "ER_IE_IMPORT_INVALID_TASK_NAME":(IMPORT_EXPORT_ERROR_BASE + 4
                                            ,"无效的任务"
                                            ,"invalid import task ")
                            , "ER_IE_IMPORT_INVALID_TASK":(IMPORT_EXPORT_ERROR_BASE + 5
                                            ,"无效的任务"
                                            ,"invalid import task ")
                            , "ER_IE_DELETE_NOT_FIND_TARGET":(IMPORT_EXPORT_ERROR_BASE + 6
                                            ,"找不到目标"
                                            ,"not find target")
                            , "ER_IE_DELETE_EXCEPTION":(IMPORT_EXPORT_ERROR_BASE + 7
                                            ,"删除异常"
                                            ,"delete exception")
                            , "ER_IE_ADD_IMPORT_TASK_EXCEPTION":(IMPORT_EXPORT_ERROR_BASE + 8
                                            ,"添加导入任务异常,文件名：%(detail_info)s"
                                            ,"add import task %(detail_info)s exception")
                            , "ER_IE_WRITE_IMPORT_FILE_EXCEPTION":(IMPORT_EXPORT_ERROR_BASE + 9
                                            ,"保存导入文件异常，文件名：%(detail_info)s"
                                            ,"write import file %(detail_info)s exception")
                            }
err_code_mgr.regist_errors(import_export_error_defs)

#用户管理错误信息
USER_MANAGEMENT_ERROR_BASE = IMPORT_EXPORT_ERROR_BASE + 0x20
user_management_error_defs = {"ER_UM_INVALID_USER_NAME":(USER_MANAGEMENT_ERROR_BASE + 0
                                            ,"无效的用户名"
                                            ,"invalid user name")
                              ,"ER_UM_USER_NAME_NOT_EXIST":(USER_MANAGEMENT_ERROR_BASE + 1
                                            ,"没有此用户"
                                            ,"user name not exist")
                              ,"ER_UM_DELETE_FAILED":(USER_MANAGEMENT_ERROR_BASE + 2
                                            ,"系统正忙"
                                            ,"delete failed")
                              ,"ER_UM_ADD_USER_INVALID_PARAMS":(USER_MANAGEMENT_ERROR_BASE + 3
                                            ,"无效的参数"
                                            ,"invalid params")
                              ,"ER_UM_ADD_USER_EXIST":(USER_MANAGEMENT_ERROR_BASE + 4
                                            ,"用户已存在"
                                            ,"user already exist")
                              ,"ER_UM_ADD_USER_FAILED":(USER_MANAGEMENT_ERROR_BASE + 5
                                            ,"添加失败:%(detail_info)s"
                                            ,"add user failed:%(detail_info)s")
                              }
err_code_mgr.regist_errors(user_management_error_defs)

#日志采集错误信息
LOG_COLLECT_ERROR_BASE = USER_MANAGEMENT_ERROR_BASE + 0x20
log_collect_error_defs = {"ER_LC_INVALID_PARAMS":(LOG_COLLECT_ERROR_BASE + 0
                                            ,"无效的参数"
                                            ,"invalid params")
                          ,"ER_LC_SYSTEM_BUSY":(LOG_COLLECT_ERROR_BASE + 1
                                            ,"系统正忙"
                                            ,"system is busy")
                          ,"ER_LC_COLLECT_EXCEPTION":(LOG_COLLECT_ERROR_BASE + 1
                                            ,"采集失败，详情：%(detail_info)s"
                                            ,"failed to collect, detail:%(detail_info)s")
                          ,"ER_LC_SERVER_EXCEPTION":(LOG_COLLECT_ERROR_BASE + 1
                                            ,"服务器异常"
                                            ,"system exception")
                          ,"ER_LC_task_EXCEPTION":(LOG_COLLECT_ERROR_BASE + 1
                                            ,"任务异常"
                                            ,"task exception")
                              }
err_code_mgr.regist_errors(log_collect_error_defs)



