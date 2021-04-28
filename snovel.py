'''
Description: 
Author: cc
Date: 2021-04-19 10:57:23
LastEditors: cc
LastEditTime: 2021-04-28 11:12:24
'''

from snovel.snovelUI import SnovalUI
from snovel.config import Config


if __name__ == "__main__":
    ui = SnovalUI("./", Config)
    ui.run()
