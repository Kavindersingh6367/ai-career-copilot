from sqlalchemy import Column,Integer,Table,String,Text,ForeignKey
from db import Base

class user(Base):
    __tablename__='users'
    
    id = Column(Integer,primary_key=True)
    email = Column(String(100),unique=True)
    password = Column(String(100),unique=True)

class Report(Base):
    __tablename__='reports'
    
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    resume_text = Column(Text)
    results = Column(Text)



