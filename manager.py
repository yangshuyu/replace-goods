import os
import re
import random

import redis
from flask_migrate import MigrateCommand
from flask_script import Manager

from api.app import create_app

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


# @manager.option('-f', '--file', dest='file_name')
# def del_part_time_users(file_name):
#     from scripts.del_part_time_user import del_part_time_users
#     del_part_time_users(file_name)


if __name__ == '__main__':
    manager.run()
