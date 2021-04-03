import os
from importlib import import_module

from app import logger, spinner
from app.intsl.Basic import Basic
from app.intsl.Migrate import Migrate


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

		if self.args.migrate is True:
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
		print("""██╗███╗   ██╗████████╗███████╗██╗         ██████╗ ██╗   ██╗
██║████╗  ██║╚══██╔══╝██╔════╝██║         ██╔══██╗╚██╗ ██╔╝
██║██╔██╗ ██║   ██║   ███████╗██║         ██████╔╝ ╚████╔╝ 
██║██║╚██╗██║   ██║   ╚════██║██║         ██╔═══╝   ╚██╔╝  
██║██║ ╚████║   ██║   ███████║███████╗    ██║        ██║   
╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝    ╚═╝        ╚═╝   """)
		print('INTSL PYへようこそ')

