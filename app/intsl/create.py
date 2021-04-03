import sys
from app.intsl.setup import Setup
import csv
import os
import re
import shutil

from sqlalchemy import and_

from app import db_manager, spinner, session, logger
from app.intsl.Basic import Basic
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
                    hit_list.append([row[0], row[1], row[2], row[3]])
            if len(hit_list) == 1:
                return hit_list[0]
            elif len(hit_list) > 1:
                use_status = await self.select_version(hit_list)
                return use_status
            else:
                exit('存在しないバージョンです')

    async def select_version(self, hit_list: list = None):
        select_status = None
        while select_status is None:
            if self.args.status is not None and select_status is None:
                select_status = self.args.status
            else:
                print(f"""このバージョンには複数のステータスが存在します、statusを入力して選択してください
- status: {hit_list[0][2]}
- version: {hit_list[0][0]}

- status: {hit_list[1][2]}
- version: {hit_list[1][0]}
""")
                select_status = input()
            for i in hit_list:
                if select_status == i[2]:
                    use_status = i
                    break
            else:
                print('存在しないステータスです')
        return use_status

    async def register(self, mc_server_name: str = None, mc_server_desc: str = None, mc_server_port: int = None, mc_server_type: str = None, mc_version_result=None):
        print(f"""最終確認: 登録内容を最後にもう一度よくご確認ください。
サーバー名: {mc_server_name}
サーバー概要: {mc_server_desc}
サーバーポート: {mc_server_port}
サーバーエディション: {mc_server_type}
サーバーバージョン: {mc_version_result[0]}
""")
        y_or_n = await Basic().text_input('本当によろしいですか?: ', ['y', 'n'])

        if y_or_n == 'n':
            logger.info('登録をキャンセルしました')
            sys.exit(0)
        check_dir = await Basic().check_dir(f'./app/server/{mc_server_name}/')
        if check_dir is True:
            logger.error(f'すでに使用されているサーバー名です')
            sys.exit(0)
        spinner.start('キャッシュを確認しています')
        tmp_path = await Basic().check_tmp()
        download_file_path = f'{tmp_path}intsl_py/{mc_server_type}/'
        download_file_name = await self.get_file_name(mc_server_type, mc_version_result)
        if os.path.exists(f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar'):
            spinner.succeed('キャッシュの確認に成功')
            sha1_hash = await Basic().check_sha1_hash(f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar')
            check_database = session.query(Hash).filter(and_(
                Hash.file_name == f'{mc_version_result[0]}_{mc_version_result[2]}.jar', Hash.sha1 == sha1_hash))
            if check_database:
                spinner.succeed('ハッシュの確認に成功')
            else:
                spinner.fail(
                    'ハッシュの確認に失敗しました。ファイルが改ざんされている可能性があります。安全のためサービスを終了します')
                sys.exit(1)
        else:
            await Basic(spinner).create_dir(download_file_path)
            jar_hash = await Basic().download_file(mc_version_result[1], download_file_path, download_file_name)
            if jar_hash == mc_version_result[3]:
                spinner.succeed('ハッシュの確認に成功')
                os.rename(f'{download_file_path}{download_file_name}',
                          f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar')
                await db_manager.commit(Hash(file_name=f'{mc_version_result[0]}_{mc_version_result[2]}.jar', sha1=jar_hash))
            else:
                spinner.fail(
                    'ハッシュの確認に失敗しました。ファイルが改ざんされている可能性があります。安全のためサービスを終了します')
                sys.exit(0)
        await Basic(spinner).create_dir(f'./app/server/{mc_server_name}')
        shutil.copy(
            f'{download_file_path}{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar', f'./app/server/{mc_server_name}/')
        await db_manager.commit(Server(name=mc_server_name, description=mc_server_desc, port=mc_server_port, path=f'./app/server/{mc_server_name}/', jar_name=f'{mc_server_type}_{mc_version_result[0]}_{mc_version_result[2]}.jar', original_jar_name=download_file_name))

        await Setup(server_name=mc_server_name, server_type=mc_server_type).run()

    async def get_file_name(self, mc_server_type: str = None, mc_version_result: list = None):
        if mc_server_type == 'official':
            download_file_name = 'server.jar'
        elif mc_server_type == 'forge':
            download_file_name = re.search(
                'https://files.minecraftforge.net/maven/net/minecraftforge/forge/(.*)/(.*)', str(mc_version_result[1])).group(2)
        else:
            download_file_name = None
        return download_file_name
