import csv
import sqlite3
from argparse import ArgumentParser
from logging import getLogger, StreamHandler, DEBUG, Formatter, addLevelName
from module.create_logger import easy_logger
from model.server import *
from setting import session

logger = getLogger(__name__)

logger = easy_logger.create(logger)


def check_list(content, list_content):
    for i in list_content:
        if content == i:
            return 0
    else:
        return 1


def check_mc_version(mc_type, mc_version):
    with open(f'data/{mc_type}.csv') as f:
        reader = csv.reader(f)
        hit_list = []
        for row in reader:
            if mc_version == row[0]:
                hit_list.append([row[0], row[1], row[2]])
        return hit_list
        # print(hit_list[0][2])


if __name__ == "__main__":
    parser = ArgumentParser(description='プログラムの説明')  # parserを定義

    # 受け取る引数を追加する
    # parser.add_argument('arg1', help='引数arg1の説明')  # 必須の引数を追加
    # parser.add_argument('arg2', help='引数arg2の説明')
    parser.add_argument('--type')  # サーバータイプ指定
    parser.add_argument('-a', '--version')  # mcバージョン指定

    args = parser.parse_args()  # 引数を解析

    # print('arg1=', args.arg1)
    # print('arg2=', args.arg2)
    mc_type = args.type
    mc_version = args.version
    print('arg3=', args.type)
    print('arg4=', args.version)

print('--------------------------------')
print('何をするか入力してください')
print('1. create')
print('2. manage')
print('3. delete')
print('--------------------------------')
what_use = input()

if what_use == 'create' or what_use == 'c':
    logger.debug('create')
    type_list = ['official', 'spigot', 'forge', 'paper', 'sponge']
    if mc_type:
        logger.debug('typeが引数で宣言されています')
    else:
        logger.debug('typeが引数で宣言されていません')
        mc_type = input('サーバータイプを入力してください: ')
    if check_list(mc_type, type_list) == 1: exit('存在しないサーバータイプです')
    if mc_version:
        logger.debug('versionが引数で宣言されています')
    else:
        logger.debug('versionが引数で宣言されていません')
        mc_version = input('サーバーバージョンを入力してください: ')
    hit_list = check_mc_version(mc_type, mc_version)
    if len(hit_list) == 1:
        print(f"""status: {hit_list[0][2]}\nversion: {hit_list[0][0]}""")
    elif len(hit_list) == 2:
        print(f"""このバージョンには複数のステータスが存在します、statusを入力して選択してください
status: {hit_list[0][2]}
version: {hit_list[0][0]}

status: {hit_list[1][2]}
version: {hit_list[1][0]}    
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
    input_server_name = None
    while input_server_name is None or len(input_server_name) == 0:
        input_server_name = input('サーバー名を入力してください: ')

    input_server_description = None
    while input_server_description is None or len(input_server_description) == 0:
        input_server_description = input('サーバーの説明を入力してください: ')

    input_server_port = None
    while input_server_port is None or not input_server_port.isdigit():
        input_server_port = input('サーバーのポートを入力してください: ')

    default_finnal_message = f"""最終確認: 本当に以下の内容で作成してよろしいですか?
name: {input_server_name}
description: {input_server_description}
port: {input_server_port}
type: {mc_type}
version: {mc_version}"""

    if len(hit_list) == 2:
        print(f"""{default_finnal_message}
    - status: {use_status[2]}
    """)
    else:
        print(f'{default_finnal_message}')
    confirm = None
    while confirm is None:
        logger.info('作成する場合は(Y)esしない場合は(N)oを入力してください')
        input_confirm = input()
        if input_confirm.lower() == 'y' or input_confirm.lower() == 'yes':
            confirm = True
        elif input_confirm.lower() == 'n' or input_confirm.lower() == 'no':
            exit('サービスを終了しています...')
        logger.info('(Y)esまたは(N)oを入力してください')
    server = Server()
    server.name = f'{input_server_name}'
    server.port = input_server_port
    server.description = f'{input_server_description}'
    session.add(server)
    session.commit()

elif what_use == 'manage' or what_use == 'm':
    input_server_name = input()
    servers = session.query(Server). \
        filter(Server.name == f'{input_server_name}'). \
        all()
    for server in servers:
        print(f'{server.name} {server.description} {server.port}')
    logger.debug('manage')
elif what_use == 'delete' or what_use == 'd':
    logger.debug('delete')
print(what_use)
