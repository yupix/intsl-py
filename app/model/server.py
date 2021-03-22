from sqlalchemy import Column, Integer, String, DateTime, Sequence
from datetime import datetime
import sys

from app import Base, Engine


class Server(Base):
	"""
	ServerModel
	"""
	__tablename__ = 'servers'
	id = Column(Integer, Sequence('server_id_seq'), primary_key=True)
	name = Column(String(50))
	port = Column(Integer)
	description = Column(String(255))
	created_at = Column('created', DateTime, default=datetime.now, nullable=False)
	updated_at = Column('modified', DateTime, default=datetime.now, nullable=False)


def main(args):
	Base.metadata.create_all(bind=Engine)


if __name__ == "__main__":
	main(sys.argv)
