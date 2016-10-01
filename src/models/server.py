from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from src.tools.database import Base

from .base import Base as BaseModel

class Server(BaseModel, Base):
	__tablename__ = 'servers'

	id = Column(Integer, primary_key=True)
	ip = Column(String(255))
	port = Column(Integer)