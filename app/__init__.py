from logging import getLogger

from halo import Halo

from .module.create_logger import EasyLogger
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

# スピナー周り
spinner = Halo(text='Loading', spinner='dots')

spinner.start("プログラムの初期化を開始します")

# ログ周り
logger_level = 'DEBUG'
logger = getLogger(__name__)
logger = EasyLogger(logger, logger_level=f'{logger_level}').create()
spinner.succeed("ログの初期化")

# データベース周り
Engine = create_engine('sqlite:///data/database/server.db', encoding="utf-8")  # DEBUG時のみecho=True
Session = sessionmaker(bind=Engine)
session = Session()
Base = declarative_base()
spinner.succeed("データベースの初期化")