#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from sqlalchemy import Column, Integer, String, DateTime, BigInteger

Base = declarative_base()

TASK_STATUS_UPLOAD = "upload"
TASK_STATUS_READY = "ready"
TASK_STATUS_RUNNING = "running"
TASK_STATUS_FINISH = "finish"
TASK_STATUS_SUSPEND = "suspend"
TASK_STATUS_ERROR = "error"


class ImportAKeyTask(Base):
    __tablename__ = 'asim_import_akey_task'
    
    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    file_name = Column(String)
    task_status = Column(String)
    
    upload_time = Column(Integer)
    start_time = Column(Integer)
    finish_time = Column(Integer)
    
    total_item = Column(Integer)
    finish_item = Column(Integer)
    failed_item = Column(Integer)


    def __repr__(self):
        return "[ImportAKeyTask(task_name='%s', file_name='%s', task_status='%s']" % (self.task_name
                                                                                                , self.file_name
                                                                                                , self.task_status)
    
