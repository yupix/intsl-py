from app.main import Basic
import os
import re
import subprocess
from app.model.server import Server
from app import session, spinner


class Setup:
    def __init__(self, server_name: str = None, server_type: str = None):
        self.server_name = server_name
        self.server_type = server_type
        self.search_server = session.query(Server).filter(
            Server.name == server_name).first()

    async def run(self):
        os.chdir(self.search_server.path)
        if self.server_type == 'official':
            await self.official()
        elif self.server_type == 'forge':
            await self.forge()

    async def official(self):
        spinner.start('サーバーを起動中です')
        command = ['java', '-jar',
                   f'{self.search_server.jar_name}']
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        for i in proc.stdout.readlines():
            print(i.decode().rstrip())
            if re.search('You need to agree to the EULA in order to run the server. Go to eula.txt for more info.', i.decode().strip()):
                spinner.succeed('Eulaの生成に成功')
                break

    async def forge(self):
        get_file_name = re.search(
            'forge_(.*)_(.*).jar', self.search_server.jar_name).group(2)
        if get_file_name == 'unstable' or get_file_name == 'stable':
            spinner.start('サーバーをセットアップ中です')
            command = ['java', '-jar',
                       f'{self.search_server.jar_name}', '--installServer']
            proc = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.wait()
            spinner.succeed('サーバーのセットアップに成功しました').start('インストーラーを削除中')
            os.remove(re.search('forge_(.*)_(.*)',
                      self.search_server.jar_name).group())
            spinner.succeed('インストーラーの削除に成功の削除に成功').start('サーバーの初回起動中')
            command = ['java', '-jar', self.search_server.original_jar_name.replace(
                '-installer.jar', '-universal.jar')]
            proc = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if re.search('You need to agree to the EULA in order to run the server. Go to eula.txt for more info.', proc.stdout.read().decode().strip()):
                await self.eula()

    async def eula(self):
        spinner.succeed('サーバーの初回起動に成功')
        y_or_n = await Basic().text_input('Minecraftエンドコンテンツ利用規約所に同意しますか: ', ['y', 'n'])
        if y_or_n == 'y':
            if os.path.exists('eula.txt'):
                with open('eula.txt', encoding="utf-8") as f:
                    data_lines = f.read()
                with open('eula.txt', mode="w", encoding="utf-8") as f:
                    f.write(data_lines.replace('eula=false', 'eula=true'))
            else:
                exit('同意しない場合は利用できません')
            return True
