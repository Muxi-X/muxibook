import time
from flask import jsonify,request,g,url_for,current_app
from .. import db
from ..models import User,Book
from . import api
from .errors import forbidden

@api.route('/book/',methods=['POST'])
def add_book(kind,bokname,boknum):
	t=request.args.get('token')
	bok=Book(kind=kind,bookname=bokname,book_num=boknum)
	db.session.add(bok)
	db.session.commit()
	response=jsonify({"msg":"add successfully"})
	response.status_code=201
	return response

@api.route('/book/',methods=['GET'])
def find_book(kind,page):


@api.route('/booklend/',methods=['POST'])
def lend_book(bokname,relname):
	t=request.args.get('token')
	usr=User.query.filter_by(realname=relname).first()
	bok=Book.query.filter_by(bookname=bokname).first()
	if usr.confirm(t) and usr.book_count <= 5:
		bok.user_id=usr.id
		bok.ava=false
		bok.date=time.local(time.time())
		usr.book_count=usr.book_count+1
		db.session.add(bok,usr)
		db.session.commit()
		response=jsonify({
			"book":bokname,
			"kind":kind,
			"available":bok.ava,
			"who":usr.username,
			"when":bok.return_time,
			"realname":usr.realname
		})
		response.status_code=200
	else:
		response=jsonify({})
		if usr.confirm(t) is False:
			response.status_code=401
		else: 
			response.status_code=403
	return response

