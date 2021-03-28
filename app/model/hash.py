from sqlalchemy import Column, Integer, String, Sequence, UniqueConstraint

from app import Base


class Hash(Base):
	"""
	HashModel
	"""
	__tablename__ = 'hashes'
	__table_args__ = (UniqueConstraint('file_name', 'sha1'),)
	id = Column(Integer, Sequence('server_id_seq'), primary_key=True)
	file_name = Column(String(60))
	sha1 = Column(String(60))
