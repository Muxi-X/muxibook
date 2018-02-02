FROM python:3.6-slim

WORKDIR /muxibook

ADD . /muxibook

RUN pip3 install -r requirements.txt

EXPOSE 80

RUN python3 manage.py shell \

&& from muxibook_app import db \

&& db.drop_all() \

&& db.create_all() \

&& quit() \

&& python3 manage.py kind_init \

&& python3 manage.py db init \

&& python3 manage.py db migrate -m "initial migration" \

&& pyhton3 manage.py db upgrade \

&& gunicorn --name muxibook -b 0.0.0.0:1488 -w 2 wsgi:app &

