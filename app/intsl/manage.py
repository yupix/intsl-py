from app import session
from app.main import Basic


class Manage:
	def __init__(self, args):
		self.args = args

	async def run(self):
		mc_server_name = await Basic().text_input('サーバー名を入力してください: ')
		search_server = session.query(name=mc_server_name).first()
		print(search_server)
