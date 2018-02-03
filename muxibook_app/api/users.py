from flask import jsonify,request,current_app,url_for
from . import api
from .. import db
from ..models import User,Book


@api.route('/login/',methods=['POST'])
def login():
    usrname=request.get_json().get('username')
    pasword=request.get_json().get('password')
    usr=User.query.filter_by(username=usrname).first()
    if usr is None or usr.verify_password(pasword)==False:
        response=jsonify({})
        response.status_code=401
        return response
    else:
        if usr.verify_password(pasword):
            token=usr.generate_confirmation_token()
            response=jsonify({"token":token})
            response.status_code=200
            return response
            
@api.route('/signup/',methods=['POST'])
def signup():
    relname=request.get_json().get('realname')
    usrname=request.get_json().get('username')
    pasword=request.get_json().get('password')
    usr=User.query.filter_by(username=usrname).first()
    if usr is not None:
        response=jsonify({})
        response.status_code=401
        return response
    else:
        usr=User(username=usrname,password=pasword,realname=relname)
        db.session.add(usr)
        db.session.commit()
        response=jsonify({"msg":"successful"})
        response.status_code=200
        return response

            
