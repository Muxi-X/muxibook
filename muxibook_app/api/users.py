import requests
from flask import jsonify,request,current_app,url_for
from . import api
from .. import db
from ..models import User,Book

headers={'Content-Type':'application/json','Accept':'application/json'}

url_login='http://auth.muxixyz.test:5499/api/login/'

url_signup='http://auth.muxixyz.test:5499/api/signip/'

@api.route('/login/',methods=['POST'])
def login():
    usrname=request.get_json().get('username')
    pasword=request.get_json().get('password')
    payload={"username":usrname,"password":pasword}
    r=requests.post(url_login,data=json.dumps(payload),headers=headers)
    if r.status_code == 200 :
        usr=User.query.filter_by(auth_id=r.json()[user_id]).first()
        token=usr.generate_confirmation_token()
        response=jsonify({"token":token})
        return response
    else :
        response=jsonify({})
        response.status_code=r.status_code
        return response
            
@api.route('/signup/',methods=['POST'])
def signup():
    relname=request.get_json().get('realname')
    usrname=request.get_json().get('username')
    pasword=request.get_json().get('password')
    email=request.get_json().get('email')
    payload={"username":usrname,"password":pasword,"email":email}
    r=requests(url_signup,data=json.dumps(payload),headers=headers)
    if r.status_code==200:
        usr=User.query.filter_by(username=usrname).first()
        usr=User(username=usrname,password='muxibooks',realname=relname,auth_id=r.json()["created"])
        db.session.add(usr)
        db.session.commit()
        response=jsonify({"msg":"successful"})
        response.status_code=200
        return response
    else :
        response=jsonify({})
        response.status_code=r.status_code
        return response

            
