from flask import jsonify,request,current_app,url_for
from . import api
from .. import db
from ..models import User,Book


@api.route('/login/',methods=['POST'])
def login():
    usrname=request.get_json().get('username')
    usr=User.query.filter_by(username=usrname).first()
    if usr is None:
        usr=User(username=usrname,password='muxibooks')
        db.session.add(usr)
        db.session.commit()
    token=usr.generate_confirmation_token()
    response=jsonify({"token":token})
    response.status_code=200
    return response
            
@api.route('/signup/',methods=['POST'])
def signup():
    usrname=request.get_json().get('username')
    user=User.query.filter_by(username=usrname).first()
    if user is not None:
        response=jsonify({})
        response.status_code=401
        return reponse
    usr=User(username=usrname,password='muxibooks')
    db.session.add(usr)
    db.session.commit()
    response=jsonify({"msg":"successful"})
    response.status_code=200
    return response

            
