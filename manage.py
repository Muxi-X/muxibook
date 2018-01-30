import sys
import os 
import time
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

from mixibook import muxibook_app

reload(sys)
sys.setdefaultencoding('utf-8')

manager=Manager(app)
migrate=Migrate(app)

def make_shell_context():
	return dict(app=app)

manage.add_command("shell",Shell(make_context=make_shell_context))

@manager.command
def test():
	"""run your unit tests"""
	import unittests
	tests=unittests.TestLoader().discover('test')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
	manager.run(debug=True)
