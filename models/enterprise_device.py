#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from sqlalchemy import Column, Integer, String, DateTime, BigInteger

Base = declarative_base()

class EnterpriseDevice(Base):
    __tablename__ = 'asim_enterprise_device'    
    id = Column(Integer, primary_key=True)
    device_serial_no = Column(String)
    device_type = Column(String)
    interface_type = Column(String)
    username = Column(String)
    bindtime = Column(Integer)
    publishtime = Column(Integer)

    def __repr__(self):
        return "[EnterpriseDevice(device_serial_no='%s', username='%s', bindtime='%s', publishtime='%s')]" % (self.device_serial_no
                                                                                                         , self.username
                                                                                                         , self.bindtime
                                                                                                         , self.publishtime)
    
