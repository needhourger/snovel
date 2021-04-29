'''
Description: 
Author: cc
Date: 2021-04-29 14:54:29
LastEditors: cc
LastEditTime: 2021-04-29 14:56:31
'''
from snovel.config import Config
from snovel.database import DataBase

if __name__ == "__main__":
    config = Config()
    db = DataBase(config)
