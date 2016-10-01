from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.tools.database import Base

from src.tools.crypt import Crypt

from .base import Base as BaseModel

class User(BaseModel, Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String(16))
	password = Column(String(16))
	nickname = Column(String(16))
	secret_question = Column(String(50))
	secret_answer = Column(String(50))
	role = Column(Integer)
	banned = relationship('BannedUser', uselist=False, backref='users')

	@staticmethod
	def encrypt_password(password, key):
		password = list(password)
		key = list(key)

		crypted_password = '1'

		for i in range(len(password)):
			pkeys = [ord(password[i]), ord(key[i])]
			hkeys = [pkeys[0] / 16, pkeys[0] % 16]
			crypted_password += Crypt.HASH[(hkeys[0] + pkeys[1]) % len(Crypt.HASH)] + Crypt.HASH[(hkeys[1] + pkeys[1]) % len(Crypt.HASH)]

		return crypted_password
