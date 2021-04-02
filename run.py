import asyncio
from argparse import ArgumentParser
from app.main import Action

if __name__ == "__main__":
    parser = ArgumentParser(description='プログラムの説明')
    parser.add_argument('-a', '--action', type=str)
    parser.add_argument('--type', type=str)
    parser.add_argument('-v', '--version')
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-d', '--desc', type=str)
    parser.add_argument('-s', '--status', type=str)
    parser.add_argument('-n', '--name', type=str)
    parser.add_argument('-y', '--auto-y', action='store_true')
    parser.add_argument('-m', '--migrate', action='store_true')
    parser.add_argument('-u', '--update', action='store_true')
    args = parser.parse_args()
    action = Action(args=args)
    asyncio.run(action.check())
