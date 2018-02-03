import time
from flask import jsonify,request,g,url_for,current_app
from .. import db
from ..models import User,Book,Kind
from . import api
from .errors import forbidden

@api.route('/book/',methods=['POST'])
def add_book():
	kind=request.get_json().get('kind')
	bokname=request.get_json().get('book')
	boknum=request.get_json().get('no')
	t=request.args.get('token')
	bok=Book(kind_id=kind,bookname=bokname,book_num=boknum)
	db.session.add(bok)
	db.session.commit()
	response=jsonify({"msg":"add successfully"})
	response.status_code=201
	return response

@api.route('/book/',methods=['GET'])
def find_book():
	page=int(request.args.get('page'))
	kind=request.args.get('kind')
	knd=Kind.query.filter_by(id=kind).first()
	counter=0
	boks=list([None,None,None,None,None,None,None,None,None,None,None])
	for b in knd.books:
		if b.ava==0:
			if (time.time()-int(b.lend_time)) > 5155199:
				b.ava=2
		counter=counter+1
		c=int(counter)//10
		if (c+1) == page:
			usr=User.query.filter_by(id=b.user_id).first()
			if usr==None:
				b.ava=1
				boks[counter%10]={
					"book":b.bookname,
					"no":b.book_num,
					"kind":b.kind_id,
					"available":b.ava
				}		
				db.session.add(b)
				db.session.commit()
			else :
				boks[counter%10]={
					"book":b.bookname,
					"no":b.book_num,
					"kind":b.kind_id,
					"available":b.ava,
					"who":usr.username,
					"when":b.return_time,
					"realname":usr.realname
				}
	response=jsonify({
		"num":counter,
		"page":page,
		"books":boks
	})
	response.status_code=200
	return response

@api.route('/booklend/',methods=['POST'])
def lend_book():
	bokname=request.get_json().get('book')
	relname=request.get_json().get('realname')
	t=request.headers.get("token")
	usr=User.query.filter_by(realname=relname).first()
	bok=Book.query.filter_by(bookname=bokname).first()
	if usr.confirm(t) and usr.book_count <= 5:
		bok.user_id=usr.id
		bok.ava=0
		a=time.localtime(time.time()+5155199)
		bok.lend_time=str(time.time())
		bok.return_time=str(a[0])+"-"+str(a[1])+"-"+str(a[2])
		usr.book_count=usr.book_count+1
		db.session.add(bok,usr)
		db.session.commit()
		response=jsonify({
			"book":bokname,
			"kind":bok.kind_id,
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

@api.route('/mybooks/',methods=['POST'])
def mybooks():
	token=request.headers.get('token')
	usrname=request.get_json().get('username')
	usr=User.query.filter_by(username=usrname).first()
	if usr.confirm(token) :
		lends=list([None,None,None,None,None,None])
		c=0
		for b in usr.books:
			c=c+1
			lends[c]={
				"no" : b.book_num,
				"bookname" : b.bookname,
				"return_time" : b.return_time				
			}
		response=jsonify({"lend":lends})
		response.status_code=200
		return response
	else:
		response=jsonify({})
		response.status_code=401
		return response
