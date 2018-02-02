# ** Muxibook **

before you use muxibook server ,you must run these code :

## step1: install requirements
	
	(venv)$ pip3 install -r requirements.txt

## step2: build your database

	(venv)$ python3 manage.py shell

	>>> from muxibook_app import db
		
	>>> db.create_all()

	>>> quit()

## step3: initialze your database

	(venv)$ python3 manage.py kind_init

	(venv)$ python3 manage.py get_info

## step4: migrate your database

	(venv)$ python3 manage.py db init

	(venv)$ python3 manage.py db migrate -m "initail migration"

	(venv)$ python3 manage.py db upgrade

## step5: open your server

	gunicorn --name muxibook -b 0.0.0.0:1488 -w 2 wsgi:app &

then you can enjoy muxibook server at 0.0.0.0:1488/api/v1.0/


