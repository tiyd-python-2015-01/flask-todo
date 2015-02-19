from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from to_do.app import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.run()
