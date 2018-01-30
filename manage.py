#coding:utf-8
import sys
import importlib
import os 
import time
from muxibook_app import create_app,db
from muxibook_app.models import User,Book,Kind
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand


importlib.reload(sys)
#export PYTHONIOENCODING = "UTF-8"

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
	return dict(app=app)

#manage.add_command("shell",Shell(make_context=make_shell_context))

@manager.command
def test():
	"""run your unit tests"""
	import unittests
	tests=unittests.TestLoader().discover('test')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
	manager.run()
	app.run(debug=True)
