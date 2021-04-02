import os
import re
import subprocess

from app import spinner


class Migrate:
	def __init__(self, commands: list = None) -> None:
		self.commands = commands

	def process(self, commands: list = None):
		if commands is None:
			command = self.commands
		else:
			command = commands
		status = None
		proc = subprocess.Popen(
			command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		while proc.poll() is None:
			log = str(proc.stdout.readline().decode('utf8'))
			if re.search("Generating (.*) done", log) or re.search('INFO\s(.*)\sRunning\supgrade\s(.*)\s->\s(.*),\s(.*)', log) or re.search('ERROR (.*) Target database is not up to date.', log):
				status = 0
				break
			elif re.search('FAILED: Can\'t locate revision identified by (.*)', log):
				status = 'revision identified error'
				break
		return status

	def generate(self):
		os.chdir('./app')
		spinner.start('migrateファイルの生成を実行中')
		generate_status = self.process()
		if generate_status == 0:
			spinner.succeed('migrateファイルの生成に成功')
			self.upgrade()
		elif generate_status == 'revision identified error':
			spinner.fail('データベースのバージョン管理システムとの整合性が損なわれています')
			exit('再度実行し問題が修正されない場合は作者へご連絡ください。')
		else:
			spinner.fail('migrateファイルの生成に失敗')
			exit('データベースが使用できないためINTSL PYを終了します')
		os.chdir('../')

	def upgrade(self):
		spinner.start('生成したmigrateファイルを適応中')
		upgrade_status = self.process(['alembic', 'upgrade', '+1'])
		if upgrade_status == 0:
			spinner.succeed('migrateファイルの適応に成功')
		else:
			spinner.fail('migrateファイルの適応に失敗しました')
			exit('再度実行し問題が修正されない場合は作者へご連絡ください')
		return 0
