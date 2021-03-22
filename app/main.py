from importlib import import_module

from app import logger


class Basic:
	def __init__(self):
		pass

	async def text_input(self, title: str = None, check_list: list = None, already_input: str = None):
		available_list = ''
		if check_list is not None:
			for _check_list in check_list:
				available_list += _check_list + ', '
		while True:
			if already_input is None:
				print(f'使用可能な選択肢: {available_list[:-1]}')
				print(title)
				input_content = input()
			else:
				input_content = already_input
			if input_content in check_list:
				break
		return input_content


class Action:
	def __init__(self, args):
		self.args = args
		self.action_list = {'create': 'app.intsl.create'}

	async def check(self):
		logger.debug(self.args)
		print('--------------------------------\n何をするか入力してください\ncreate\nmanage\ndelete\n--------------------------------')
		what_use = input()
		if what_use in self.action_list:
			action = {'name': f'{what_use}', 'path': f'{self.action_list[what_use]}'}
		else:
			action = None

		if action is not None:
			module = import_module(action['path'])
			cls = getattr(module, 'Create')(self.args)
			await getattr(cls, 'run')()
