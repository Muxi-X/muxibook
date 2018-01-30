import time
from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin

class User(UserMixin,db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Colunm(db.String(20),unique=True)
	realname=db.Colunm(db.String(10))
	password=db.Colunm(db.String(20))
	password_hash=db.Colunm(db.String(128))
	confirmed=db.Colunm(db.Boolean,default=False)
	book_count=db.Colunm(db.Integer,default=0)
	books=db.relationship('Book',backref='user',lazy='dynamic')
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)
	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)
#	def to_json(self):
#		json_user={
#			'url':url_for('api.get_user',id=self.id,_external=True),
#			'username':self.username,
#			'realname':self.realname,
#			'book':self.books
#		}
#		return json_user
	def generate_auth_token(self,expiration):
		s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
		return s.dumps({'id':self.id})
	@staticmethod
	def verify_auth_token(token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return None
		return User.query.get(data['id'])
	def generate_confirmation_token(self,expiration=3600):
		s=Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'confirm':self.id})
	def confirm(self,token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return False
		if data.get('confirm')!=self.id
			return False
		self.confirm=True
		db.session.add(self)
		return True


class Book(db.Model):
	__tablename__='books'
	id=db.Colunm(db.Integer,primary_key=True)
	kind=db.Colunm(db.Integer)
	bookname=db.Colunm(db.String(30))
	book_num=db.Colunm(db.String)
	ava=db.Colunm(db.Boolean)
	user_id=db.Colunm(db.Integer,db.ForeirnKey('users.id'))
	date=db.Colunm(db.DateTime)
	return_time=db.Colunm(db.String)
#	def to_json(self):
#		json_book={
#			'url':url_for('api.get_book',id=self.id,_external=True)
#			'kind':self.kind
#			'bookname':self.bookname
#			'book_num':self.book_num
#			'ava':self.ava
#			'user_id':self.user_id
#			'date'=self.date
#		} 
	@date.setter
	def ddl(self,date):
		ddl=self.date[1]+2
		self.return_time=time.asctime(ddl)
