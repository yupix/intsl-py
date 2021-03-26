from sqlalchemy import Column, Integer, String, Sequence, UniqueConstraint

from app import Base


class Hash(Base):
	"""
	HashModel
	"""
	__tablename__ = 'hashes'
	__table_args__ = (UniqueConstraint('file_name', 'md5'),)
	id = Column(Integer, Sequence('server_id_seq'), primary_key=True)
	file_name = Column(String(60))
	md5 = Column(String(60))
