import getpass
import hashlib
import os
import platform
import tempfile
import urllib.request
from importlib import import_module

from app import logger, spinner
from app.intsl.Migrate import Migrate


class Basic:
	def __init__(self, custom_spinner=None):
		self.use_os = None
		self.user_name = None
		self.spinner = custom_spinner

	async def check_os(self):
		use_os = os.name
		return use_os

	async def check_platform(self):
		use_platform = platform.system()
		return use_platform

	async def get_os_user_name(self):
		user_name = getpass.getuser()
		return user_name

	async def check_tmp(self):
		use_os = await self.check_os()
		if use_os == 'nt':
			user_name = await self.get_os_user_name()
			path = f'C:/Users/{user_name}/AppData/Local/Temp/'
		elif use_os == 'posix':
			path = '/tmp/'
		else:
			path = None
		return path

	async def create_tmp_dir(self):
		tmp_dir = tempfile.mkdtemp()
		return tmp_dir

	async def download_file(self, url: str, save_path: str = None, file_name: str = None):
		file_path_name = f'{save_path}{file_name}'
		spinner.start('ファイルをダウンロードしています')
		urllib.request.urlretrieve(url, file_path_name)
		spinner.succeed('ファイルのダウンロードに成功')
		checksum = await self.check_sha1_hash(file_path_name)
		return checksum

	async def check_sha1_hash(self, file_path_name):
		with open(f'{file_path_name}', 'rb') as f:
			checksum = hashlib.sha1(f.read()).hexdigest()
			return checksum

	async def check_md5_hash(self, file_path_name):
		with open(f'{file_path_name}', 'rb') as f:
			checksum = hashlib.md5(f.read()).hexdigest()
			return checksum

	async def check_dir(self, file_path):
		if os.path.isdir(file_path):
			exist = True
		else:
			exist = False
		return exist

	async def create_dir(self, file_path):
		if not os.path.isdir(file_path):
			os.makedirs(file_path)
			self.spinner.succeed('ファイルの作成に成功しました')
		else:
			self.spinner.succeed('ファイルの確認に成功しました')
		return 'succeed'

	async def text_input(self, title: str = None, check_list: list = [], already_input: str = None, return_type: type = None, custom_input: str = '>'):
		available_list = ''
		if check_list is not None:
			for _check_list in check_list:
				available_list += _check_list + ', '
		while True:
			if already_input is None:
				print(f'使用可能な選択肢: {available_list[:-1]}')
				print(title)
				try:
					input_content = input(custom_input)
				except EOFError:
					input_content = None
				if return_type:
					if return_type == str:
						input_content = str(input_content)
				elif return_type == int:
					input_content = int(input_content)
				if check_list is not None and input_content in check_list or check_list is None and input_content:
					break
			else:
				input_content = already_input
				if input_content in check_list:
					break
		return input_content


class Action:
	def __init__(self, args):
		self.args = args
		self.action_list = {'create': 'app.intsl.create',
		                    'manage': 'app.intsl.manage'}
		self.dict_action_list = ['create', 'manage']

	async def check(self):
		spinner.stop()
		logger.debug(self.args)
		if not os.path.exists('./db/intsl_py.db'):
			self.first_launch()

		if self.args.migrate is not None:
			command = ['alembic', 'revision', '--autogenerate', '-m', '\"init\"']
			Migrate(command).generate()

		print('--------------------------------\n何をするか入力してください\ncreate\nmanage\ndelete\n--------------------------------')
		if not self.args.action:
			what_use = str(await Basic().text_input('何をするか入力してください: ', self.dict_action_list))
		else:
			what_use = str(self.args.action)
		if what_use in self.action_list:
			action = {'name': f'{what_use}',
			          'path': f'{self.action_list[what_use]}'}
		else:
			action = None
		class_name = [k for k, v in self.action_list.items(
		) if v == self.action_list[what_use]][0]
		if action is not None:
			module = import_module(action['path'])
			cls = getattr(module, f'{class_name}'.capitalize())(self.args)
			await getattr(cls, 'run')()

	def first_launch(self):
		print('INTSL PYへようこそ！')
