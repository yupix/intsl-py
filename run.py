import asyncio
import csv
from argparse import ArgumentParser
from app.main import Action


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
			if mc_version in row[0]:
				hit_list.append([row[0], row[1], row[2]])
		return hit_list


if __name__ == "__main__":
	parser = ArgumentParser(description='プログラムの説明')  # parserを定義
	# 受け取る引数を追加する
	# parser.add_argument('arg1', help='引数arg1の説明')  # 必須の引数を追加
	# parser.add_argument('arg2', help='引数arg2の説明')
	parser.add_argument('--type')  # サーバータイプ指定
	parser.add_argument('-a', '--version')  # mcバージョン指定

	args = parser.parse_args()  # 引数を解析

	mc_type = args.type
	mc_version = args.version
	print('arg3=', args.type)
	print('arg4=', args.version)

	action = Action(args=args)
	asyncio.run(action.check())
