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
    b=Book.query.filter_by(book_num=boknum).first()
    if b is None:
        t=request.args.get('token')
        bok=Book(kind_id=kind,bookname=bokname,book_num=boknum)
        db.session.add(bok)
        db.session.commit()
        response=jsonify({"msg":"add successfully"})
        response.status_code=200
        return response
    else :
        response=jsonify({})
        response.status_code=400
        return response

@api.route('/book/',methods=['GET'])
def find_book():
    page=1
    if request.args.get('page') is not None:
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
    if usr.confirm(t) and usr.book_count < 5:
        bok.user_id=usr.id
        bok.ava=0
        a=time.localtime(time.time()+5155199)
        bok.lend_time=str(int(time.time()))
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
        if usr.book_count == 5:
            response.status_code=403
        else: 
            response.status_code=401
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

@api.route('/return/',methods=['POST'])
def return_book():
    book_num=request.get_json().get('no')
    username=request.get_json().get('username')
    bok=Book.query.filter_by(book_num=book_num).first()
    usr=User.query.filter_by(username=username).first()
    usr.book_count-=1
    bok.user_id=None
    bok.ava=1
    bok.return_time=None
    bok.lend_time=None
    db.session.add(bok)
    db.session.add(usr)
    db.session.commit()
    response=jsonify({})
    response.status_code=200
    return response

@api.route('/renew/',methods=['POST'])
def renew():
    book_num=request.get_json().get('no')
    username=request.get_json().get('username')
    lend_time=int(bok.lend_time)
    if (lend_time+4924800) < int(time.time()) and (lend_time+5155199) > int(time.time()):
        a=time.local(time.time()+5155199)
        bok=Book.query.filter_by(book_num=book_num).first()
        bok.lend_time=str(time.time())
        bok.return_time=str(a[0])+"-"+str(a[1])+"-"+str(a[2])
        db.session.add(bok)
        db.session.commit()
        response=jsonify({})
        response.status_code=200
        return response
    else :
        response=jsonify({})
        response.status_code=401
        return response
    
