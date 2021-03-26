from sqlalchemy import Column, Integer, String, Sequence

from app import Base


class Hash(Base):
	"""
	HashModel
	"""
	__tablename__ = 'hashes'
	id = Column(Integer, Sequence('server_id_seq'), primary_key=True)
	file_name = Column(String(60))
	md5 = Column(String(60))
