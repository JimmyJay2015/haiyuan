#coding=utf-8
'''
Created on 2014-10-13

@author: Administrator
'''

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

LOG_COLLECTION_READY = 'ready'
LOG_COLLECTION_START = 'start'
LOG_COLLECTION_STOP = 'stop'

class log_collection(Base):
    __tablename__ = 'asim_user_log_collection'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    logurl = Column(String)
    status = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    finish_time = Column(String)
    
    def __repr__(self):
        return "[log_collection(id='%s', username='%s', logurl='%s', status='%s')]" % (self.id, self.username
                                                                        , self.logurl,self.status)