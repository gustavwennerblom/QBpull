from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class TestObject(Base):
    __tablename__ = 'Test'
    idx = Column(Integer, primary_key=True)
    name = Column(String(50))
