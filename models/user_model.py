#coding=utf-8

from lxml import etree
import logging

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'ofuser'    
    username = Column(String, primary_key=True)
    name = Column(String)    
    creationdate = Column(String)
    modificationdate = Column(String)
    
    vcard = relationship("Vcard", backref="ofuser")
    
    def parsevcard(self):
        self.nickname = ''
        self.sex = ''
        self.remark = ''
        self.security_status = ''
        self.binding = 'false'
        self.region = ''
        self.photo_base64 = ''
        self.photo_type = ''
        
        #需要导出的非表字段
        out_dict = {'nickname' : '',
                'sex' : '',
                'remark' : '',
                'security_status' : '',
                'binding' : '',
                'region' : '',
                'photo_base64' : '',
                'photo_type' : '',}
        
        if len(self.vcard)>0:
            try:
                vcard2 = etree.fromstring(self.vcard[0].vcard)
                for item in vcard2:
                    if item.tag.find("NICKNAME")>=0:
                        self.nickname = item.text
                        out_dict['nickname'] = self.nickname
                    elif item.tag.find("sex")>=0:
                        self.sex = item.text
                        out_dict['sex'] = self.sex
                    elif item.tag.find("remark")>=0:
                        self.remark = item.text
                        out_dict['remark'] = self.remark
                    elif item.tag.find("security_status")>=0:
                        self.security_status = item.text
                        out_dict['security_status'] = self.security_status
                    elif item.tag.find("binding_ID")>=0:
                        if len(item.text)>0:
                            self.binding = 'true'
                        out_dict['binding'] = self.binding
                    elif item.tag.find("ADR")>=0:
                        for child in item:
                            if child.tag.find("REGION")>=0:
                                self.region = child.text
                                out_dict['region'] = self.region
                                break                     
                    elif item.tag.find("PHOTO")>=0:
                        for child in item:
                            if child.tag.find("BINVAL")>=0:
                                self.photo_base64 = child.text
                                out_dict['photo_base64'] = self.photo_base64
                            elif child.tag.find("TYPE")>=0:
                                self.photo_type = child.text
                                out_dict['photo_type'] = self.photo_type
            except Exception, e:
                logging.error(e)
            
        return out_dict
    
class Vcard(Base):
    __tablename__ = 'ofvcard'
    username = Column(String, ForeignKey('ofuser.username'), primary_key=True)
    vcard = Column(String)
    
                    
            
            
        
        
    
        
