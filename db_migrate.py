"""
数据库同步使用
@File    : db_migrate.py
$ python db_migrate.py db init
$ python db_migrate.py db migrate
$ python db_migrate.py db upgrade
$ python db_migrate.py db --help
"""

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import db, app

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manage.run()
