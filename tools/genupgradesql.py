#coding=utf-8
"""
本脚本用来从hsqldb的 openfire.script 生成插入到mysql的数据。
主要处理包括：
1，过滤非insert数据
2，在insert前插入delete数据
3，表名的大小写转换
4，\uxxxx表示的字符串转换为utf-8编码的字符串
5，在插入结束后记录插入的条数，便于升级成功以后的核查

输入参数：
源文件    目标文件   数据库名
"""

import sys


#要把script脚本中的全大写的表名全部转换为实际的大小写的表名
table_map ={"OFGROUP":"ofGroup",
"OFGROUPPROP":"ofGroupProp",
"OFGROUPUSER":"ofGroupUser",
"OFID":"ofID",
"OFOFFLINE":"ofOffline",
"OFPRESENCE":"ofPresence",
"OFPRIVATE":"ofPrivate",
"OFUSER":"ofUser",
"OFUSERPROP":"ofUserProp",
"OFUSERFLAG":"ofUserFlag",
"OFROSTER":"ofRoster",
"OFROSTERGROUPS":"ofRosterGroups",
"OFPRIVACYLIST":"ofPrivacyList",
"OFVCARD":"ofVCard",
"OFVERSION":"ofVersion",
"OFPROPERTY":"ofProperty",
"OFEXTCOMPONENTCONF":"ofExtComponentConf",
"OFREMOTESERVERCONF":"ofRemoteServerConf",
"OFSECURITYAUDITLOG":"ofSecurityAuditLog",
"OFMUCSERVICE":"ofMucService",
"OFMUCSERVICEPROP":"ofMucServiceProp",
"OFMUCROOM":"ofMucRoom",
"OFMUCROOMPROP":"ofMucRoomProp",
"OFMUCAFFILIATION":"ofMucAffiliation",
"OFMUCMEMBER":"ofMucMember",
"OFMUCCONVERSATIONLOG":"ofMucConversationLog",
"OFPUBSUBNODE":"ofPubsubNode",
"OFPUBSUBNODEJIDS":"ofPubsubNodeJIDs",
"OFPUBSUBNODEGROUPS":"ofPubsubNodeGroups",
"OFPUBSUBAFFILIATION":"ofPubsubAffiliation",
"OFPUBSUBITEM":"ofPubsubItem",
"OFPUBSUBSUBSCRIPTION":"ofPubsubSubscription",
"OFPUBSUBDEFAULTCONF":"ofPubsubDefaultConf",}

#monitor service 插件生成的表，需要忽略
ignore_tables = set(['OFCONVERSATION',
'OFCONPARTICIPANT',
'OFMESSAGEARCHIVE',
'OFRRDS'])

if __name__ == "__main__":
    if len(sys.argv)!=4:
        print "input parameters: srcpath destpath database"
        exit()
        
    srcpath = sys.argv[1]
    destpath = sys.argv[2]
    database = sys.argv[3]
    srcfile = file(srcpath)
    destfile = file(destpath, 'w')
    destfile.write('use %s;\n'%database)
    
    old_table_name = ''
    
    record_count = 0
    while True:
        line = srcfile.readline()
        
        if len(line)==0:
            break
        
        #过滤非INSERT 
        if line.find('INSERT') !=0:
            continue
        else:
            index = len('INSERT INTO ')
            subline = line[index:]
            index = subline.find(' ')
            new_table_name = subline[:index]
            
            #忽略不需要的表
            if new_table_name in ignore_tables:
                continue
            
            new_table_name = table_map[new_table_name]
            
            #为了加上最后的;先去掉最后的换行符号
            subline = subline[index:].strip('\n')
            
            #处理hsqldb 的 \u 字符串 到 utf-8的字符串
            index = subline.find('\\u')
            head = ''
            while index>=0:                
                head += subline[:index]
                subline = subline[index:]
                
                #取unicode 4个字符
                charset = "u'%s'"%(subline[0:6])                
                char = eval(charset)
                
                head += unicode(char).encode('utf-8')
                subline = subline[6:]
                index = subline.find('\\u')
            head += subline
            
            insert_sql = 'INSERT INTO `%s` %s;\n'%(new_table_name, head)
            #处理表的第一条insert
            if old_table_name!=new_table_name:
                
                #先把上一张表的记录数记录下来
                if old_table_name!='':
                    count_line = '/*%s insert records :%s*/\n\n'%(old_table_name, record_count)
                    destfile.write(count_line)                    
                                                
                old_table_name=new_table_name
                delete_sql = 'DELETE FROM `%s`;\n'%old_table_name
                destfile.write(delete_sql)
                
                #记录数先清零
                record_count = 0
                
            record_count += 1            
            destfile.write(insert_sql)
        
    destfile.close()
    srcfile.close()
                
        
        
            
        
        
    
    
    
    