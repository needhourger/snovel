'''
Description: 
Author: cc
Date: 2021-04-20 17:56:14
LastEditors: cc
LastEditTime: 2021-04-29 16:46:51
'''
import os
import pathlib


class Config:

    HOME_PATH = os.path.join(pathlib.Path.home(), ".snovel")
    DEFAULT_PATH = "./"
    # file size limit KB
    FILE_SIZE_LIMIT = 200

    # SQLITE
    DATABASE_PATH = "snovel.db"

    @classmethod
    def __init__(self) -> None:
        if not os.path.exists(self.HOME_PATH):
            os.makedirs(self.HOME_PATH)

    @property
    def DATABASE_URI(self):
        return "sqlite:///"+os.path.join(self.HOME_PATH, self.DATABASE_PATH)
