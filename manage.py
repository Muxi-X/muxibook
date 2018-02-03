#coding:utf-8
import sys
import importlib
import os 
import time
import xlrd
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

class get_info(Command):
	def run(self):
		book=xlrd.open_workbook("1.xls")
		sheets=book.sheets()
		for sheet in sheets:
			rows=sheet.get_rows()
			c=0
			for row in rows :
				c+=1
				if c>1:
					s=row[2].value.encode('utf-8').decode('utf-8')
					a=Book(ava=1,kind_id=row[0].value,book_num=row[1].value,bookname=s)
					db.session.add(a)
					db.session.commit()
		print ("successful!")

manager.add_command('get_info',get_info())

class kind_init(Command):
	def run(self):
		a=Kind()
		b=Kind()
		c=Kind()
		d=Kind()
		e=Kind()
		f=Kind()
		db.session.add(a)
		db.session.add(b)
		db.session.add(c)
		db.session.add(d)
		db.session.add(e)
		db.session.add(f)
		db.session.commit()

manager.add_command('kind_init',kind_init())	
	
def make_shell_context():
	return dict(app=app)

manager.add_command("shell",Shell(make_context=make_shell_context))

@manager.command
def test():
	"""run your unit tests"""
	import unittest
	tests=unittest.TestLoader().discover('test')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
	manager.run()
	app.run(debug=True)
