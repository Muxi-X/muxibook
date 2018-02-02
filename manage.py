#coding:utf-8
import sys
import importlib
import os 
import time
from muxibook_app import create_app,db
from muxibook_app.models import User,Book,Kind
from flask_script import Manager,Shell,Command
from flask_migrate import Migrate,MigrateCommand


importlib.reload(sys)
#export PYTHONIOENCODING = "UTF-8"

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate=Migrate(app,db)

manager.add_command('db',MigrateCommand)

def kind_init(Command):
	a=Kind()
	b=Kind()
	c=Kind()
	d=Kind()
	e=Kind()
	db.session.add(a)
	db.session.add(b)
	db.session.add(c)
	db.session.add(d)
	db.session.add(e)
	db.session.commit()

manager.add_command('kind_init',kind_init())	
	
def make_shell_context():
	return dict(app=app)

manager.add_command("shell",Shell(make_context=make_shell_context))

@manager.command
def test():
	"""run your unit tests"""
	import unittests
	tests=unittests.TestLoader().discover('test')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
	manager.run()
	app.run(debug=True)
