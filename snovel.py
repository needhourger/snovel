'''
Description: 
Author: cc
Date: 2021-04-19 10:57:23
LastEditors: cc
LastEditTime: 2021-04-29 17:59:24
'''

from snovel.snovelUI import SnovalUI
from snovel.config import Config
from snovel.database import DataBase

import os
import argparse

parser = argparse.ArgumentParser(
    description="A python based shell text novel reader")

parser.add_argument("-a", "--add", nargs='+',
                    help="add book to shelf;eg. --add ./test1.txt")
parser.add_argument("-l", "--list", action="store_true", help="list books",)
parser.add_argument("-d", "--delete", nargs="+",
                    help="delete book by id;eg. --delete 1 2 3")


if __name__ == "__main__":
    # ui = SnovalUI("./", Config)
    # ui.run()
    config = Config()
    db = DataBase(config)

    args = parser.parse_args()
    if args.list:
        db.list_books()
    elif args.add:
        for path in args.add:
            if os.path.exists(path):
                if os.path.isdir(path):
                    for root, _, files in os.walk(path):
                        for f in files:
                            p = os.path.join(root, f)
                            db.add_book(p)
                else:
                    db.add_book(path)
    elif args.delete:
        db.delete_book(args.delete)
    else:
        ui = SnovalUI(db, config)
        ui.run()
