from app import spinner
from app.intsl.Migrate import Migrate


class FirstSetup:
	def __init__(self):
		pass

	def first_launch(self):
		print("""██╗███╗   ██╗████████╗███████╗██╗         ██████╗ ██╗   ██╗
██║████╗  ██║╚══██╔══╝██╔════╝██║         ██╔══██╗╚██╗ ██╔╝
██║██╔██╗ ██║   ██║   ███████╗██║         ██████╔╝ ╚████╔╝ 
██║██║╚██╗██║   ██║   ╚════██║██║         ██╔═══╝   ╚██╔╝  
██║██║ ╚████║   ██║   ███████║███████╗    ██║        ██║   
╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝    ╚═╝        ╚═╝   """)
		print('INTSL PYへようこそ！初回起動の為少々セットアップに時間がかかる可能性があります...')
		spinner.start('データベースの作成を行います')
		# Ensure the database schema is created and up-to-date based on existing migrations
		Migrate(['alembic', 'upgrade', 'head']).generate()
		# Then, generate the initial revision if necessary
		Migrate(['alembic', 'revision', '--autogenerate', '-m', 'Initial auto-generated revision']).generate()
		spinner.succeed('データベースの作成に成功しました')
