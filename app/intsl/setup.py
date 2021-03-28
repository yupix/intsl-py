import os
import re
import subprocess
from app.model.server import Server
from app import session, spinner

class Setup:
    def __init__(self, server_name: str = None, server_type: str = None):
        self.server_name = server_name
        self.server_type = server_type

    async def run(self):
        search_server = session.query(Server).filter(Server.name == self.server_name).first()
        os.chdir(search_server.path)
        if self.server_type == 'official':
            print('official')
        elif self.server_type == 'forge':
            get_file_name = re.search('forge_(.*)_(.*).jar', search_server.jar_name).group(2)
            if get_file_name == 'unstable' or get_file_name == 'stable':
                spinner.start('サーバーをセットアップ中です')
                command = ['java', '-jar', f'{search_server.jar_name}', '--installServer']
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc.wait()
                spinner.succeed('サーバーのセットアップに成功しました').start('インストーラーを削除中')
                os.remove(re.search('forge_(.*)_(.*)', search_server.jar_name).group())
                spinner.succeed('インストーラーの削除に成功の削除に成功')
