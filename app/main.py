import os
from importlib import import_module

from app import logger, spinner
from app.intsl.Basic import Basic
from app.intsl.Migrate import Migrate
from app.intsl.firstsetup import FirstSetup


class Action:
	def __init__(self, args):
		self.args = args
		self.action_list = {'create': 'app.intsl.create',
		                    'manage': 'app.intsl.manage'}
		self.dict_action_list = ['create', 'manage']

	async def check(self):
		spinner.stop()
		if not os.path.exists('./app/db/intsl_py.db'):
			FirstSetup().first_launch()
		if self.args.migrate is True:
			# Ensure the database is up-to-date with existing migrations first
			Migrate(['alembic', 'upgrade', 'head']).generate()
			# Then, generate a new revision for any further changes
			Migrate(['alembic', 'revision', '--autogenerate', '-m', 'Auto-generated migration from Action.check']).generate()

		print('--------------------------------\n何をするか入力してください\ncreate\nmanage\n--------------------------------')
		if not self.args.action:
			what_use = str(await Basic().text_input('何をするか入力してください: ', self.dict_action_list))
		else:
			what_use = str(self.args.action)

		if what_use not in self.action_list:
			logger.error(f"Invalid action specified: {what_use}. Please choose from {list(self.action_list.keys())}.")
			return

		action = {'name': f'{what_use}',
		          'path': f'{self.action_list[what_use]}'}
		# The following line is safe now because we've validated what_use
		class_name = what_use # Simplified: class_name is just what_use if it's a valid key
		
		# action will always be not None here due to the check above, 
		# but keeping the structure for clarity or future changes where action might be None for other reasons.
		if action is not None: 
			module = import_module(action['path'])
			cls = getattr(module, f'{class_name}'.capitalize())(self.args)
			await getattr(cls, 'run')()
