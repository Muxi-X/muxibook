FROM python:3.6

WORKDIR /mb

ADD . /mb

RUN pip3 install -r requirements.txt

EXPOSE 1488

CMD ["python3","muxibook/manage.py","shell"]       \
&&  ["from","muxibook/app","import","db"]          \
&&  ["db.drop_all()"]                              \
&&  ["db.create_all()"]                            \
&&  ["quit()"]                                     \
&&  ["python3","muxibook/manage.py","kind_init"]   \
&&  ["python3","muxibook/manage.py","get_info"]    \
&&  ["python3","muxibook/manage.py","db","init"]   \
&&  ["python3","muxibook/manage.py","db","migrate","-m",""initail migrations""] \
&&  ["python3","muxibook/manage.py","db","upgrade"]\
&&  ["gunicorn","--name","muxibook","-b","0.0.0.0:1488","-w","2","wsgi:app","&"]
