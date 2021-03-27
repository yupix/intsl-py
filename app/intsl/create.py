import csv
import os
import re
import shutil

from sqlalchemy import and_

from app import db_manager, spinner, session
from app.main import Basic
from app.model.hash import Hash
from app.model.server import Server


class Create:
	def __init__(self, args=None):
		self.args = args
		self.editions = ['official', 'spigot', 'forge', 'paper', 'sponge']

	async def run(self):
		mc_server_name = self.args.name
		mc_server_desc = self.args.desc
		mc_server_port = self.args.port
		mc_version = self.args.version
		mc_server_type = self.args.type

		if self.args.type is None:
			mc_server_type = await Basic().text_input('サーバータイプを入力してください: ', self.editions)
		else:
			mc_server_type = await Basic().text_input('サーバータイプを入力してください: ', self.editions, mc_server_type)
		print(mc_server_type)
		if self.args.version is None:
			mc_version = await Basic().text_input("バージョンを入力してください")
		mc_version_result = await self.check_version(mc_server_type, mc_version)
		if self.args.name is None:
			mc_server_name = await Basic().text_input("サーバー名を入力してください")
		if self.args.desc is None:
			mc_server_desc = await Basic().text_input("サーバーの概要を入力してください")
		if self.args.port is None:
			mc_server_port = await Basic().text_input("サーバーのポートを入力してください", return_type=int)
		await self.register(mc_server_name, mc_server_desc, mc_server_port, mc_server_type, mc_version_result)

	async def check_version(self, mc_server_type, mc_version):
		with open(f'./app/data/{mc_server_type}.csv') as f:
			reader = csv.reader(f)
			hit_list = []
			for row in reader:
				if mc_version in row[0]:
					hit_list.append([row[0], row[1], row[2], row[3], row[4]])
			if len(hit_list) == 1:
				return hit_list
			elif len(hit_list) > 1:
				use_status = await self.select_version(hit_list)
				return use_status
			else:
				exit('存在しないバージョンです')

	@staticmethod
	async def select_version(hit_list):
		print(f"""このバージョンには複数のステータスが存在します、statusを入力して選択してください
- status: {hit_list[0][2]}
- version: {hit_list[0][0]}
		
- status: {hit_list[1][2]}
- version: {hit_list[1][0]}
""")
		use_status = None
		while use_status is None:
			select_status = input()
			for i in hit_list:
				if select_status == i[2]:
					use_status = i
					break
			else:
				print('存在しないステータスです')
		return use_status

	@staticmethod
	async def register(mc_server_name: str = None, mc_server_desc: str = None, mc_server_port: int = None, mc_server_type: str = None, mc_version_result=None):
		print(f"""最終確認: 登録内容を最後にもう一度よくご確認ください。
サーバー名: {mc_server_name}
サーバー概要: {mc_server_desc}
サーバーポート: {mc_server_port}
サーバーエディション: {mc_server_type}
サーバーバージョン: {mc_version_result[0]}
""")
		y_or_n = await Basic().text_input('本当によろしいですか?: ', ['y', 'n'])

		if y_or_n == 'n':
			exit('登録をキャンセルしました。')

		spinner.start('キャッシュを確認しています')
		tmp_path = await Basic().check_tmp()
		download_file_path = f'{tmp_path}intsl_py/{mc_server_type}/'
		download_file_name = re.search('https://files.minecraftforge.net/maven/net/minecraftforge/forge/(.*)/(.*)', str(mc_version_result[1])).group(2)
		if os.path.exists(f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar'):
			spinner.succeed('キャッシュの確認に成功')
			md5_hash = await Basic().check_md5_hash(f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar')
			check_database = session.query(Hash).filter(and_(Hash.file_name == f'{mc_version_result[0]}_{mc_version_result[2]}.jar', Hash.md5 == md5_hash))
			if check_database:
				spinner.succeed('ハッシュの確認に成功')
			else:
				spinner.fail('ハッシュの確認に失敗しました。ファイルが改ざんされている可能性があります。安全のためサービスを終了します')
				exit(1)
		else:
			await Basic(spinner).create_dir(download_file_path)
			jar_hash = await Basic().download_file(mc_version_result[1], download_file_path, download_file_name)
			if jar_hash == mc_version_result[3]:
				spinner.succeed('ハッシュの確認に成功')
				os.rename(f'{download_file_path}{download_file_name}', f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar')
				await db_manager.commit(Hash(file_name=f'{mc_version_result[0]}_{mc_version_result[2]}.jar', md5=jar_hash))
			else:
				spinner.fail('ハッシュの確認に失敗しました。ファイルが改ざんされている可能性があります。安全のためサービスを終了します')
				exit(1)
		await Basic(spinner).create_dir(f'./app/server/{mc_server_name}')
		shutil.copy(f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar', f'./app/server/{mc_server_name}/')

		await db_manager.commit(Server(name=mc_server_name, description=mc_server_desc, port=mc_server_port))
