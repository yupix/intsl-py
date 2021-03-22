from app.main import Basic


class Create:
	def __init__(self, args=None):
		self.args = args
		self.editions = ['official', 'spigot', 'forge', 'paper', 'sponge']

	async def run(self):
		if self.args.type is None:
			mc_type = await self.check_edition()
		else:
			mc_type = await Basic().text_input('サーバータイプを入力してください: ', self.editions, self.args.type)
		print(mc_type)

	async def check_edition(self):
		mc_type = await Basic().text_input('サーバータイプを入力してください: ', self.editions)
		return mc_type
