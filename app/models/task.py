from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasksToDo"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
