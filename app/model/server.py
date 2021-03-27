from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Sequence

from app import Base


class Server(Base):
	"""
	ServerModel
	"""
	__tablename__ = 'servers'
	id = Column(Integer, Sequence('server_id_seq'), primary_key=True)
	name = Column(String(50))
	port = Column(Integer)
	description = Column(String(255))
	path = Column(String(255))
	created_at = Column('created', DateTime, default=datetime.now, nullable=False)
	updated_at = Column('modified', DateTime, default=datetime.now, nullable=False)
