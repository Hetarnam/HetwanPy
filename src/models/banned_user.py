from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.tools.database import Base

from .base import Base as BaseModel


class BannedUser(BaseModel, Base):
	__tablename__ = 'banned_users'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	reason = Column(String)
	time_end = Column(DateTime)