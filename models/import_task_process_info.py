#coding=utf-8

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from sqlalchemy import Column, Integer, String, DateTime, BigInteger

Base = declarative_base()



class ImportTaskProcessInfo(Base):
    __tablename__ = 'asim_import_task_process_info'
    id = Column(Integer, primary_key=True)
    import_task_id = Column(Integer)
    task_name = Column(String)
    file_name = Column(String)
    
    upload_time = Column(Integer)
    finish_time = Column(Integer)
    
    
    
    total_item = Column(Integer)
    failed_item = Column(Integer)
    
    failed_info = Column(String)


    def __repr__(self):
        return "[ImportAKeyTask(task_name='%s', file_name='%s', task_status='%s']" % (self.task_name
                                                                                                , self.file_name
                                                                                                , self.task_status)
    
