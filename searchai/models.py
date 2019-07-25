from searchai import db, login_manager
# from flask_mongoengien import BaseQueryQuerySetSet
from datetime import datetime
from flask import current_app
from flask_login import UserMixin, logout_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
# @login_manager.user_loader
# def loader_user(user_email): 
#     return User.objects.get(email=user_email) 

@login_manager.user_loader
def load_user(user_id): 
    return User.objects.filter(email=user_id).first() 

class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()
 
class User(db.Document, UserMixin,JsonSerializable):
    # query_class = UserModel
    email = db.StringField(max_length=50,required=True, primary_key=True)
    username = db.StringField(max_length=50,required=True)
    image_file = db.StringField(max_length=50,required=True,default='avatar.png')
    password = db.StringField(max_length=100,required=True)
    role = db.StringField(max_length=100,required=True)
    type = db.StringField(required=True, default='none', max_length=10)

    # get code token for reset password
    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def get_login_token(self, expires_sec = 600):
        s = Serializer(current_app.config['SECRET_KEY']+'login', expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.objects.filter(email=user_id).first()

    @staticmethod
    def verify_login_token(token):
        s = Serializer(current_app.config['SECRET_KEY']+'login')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.objects.filter(email=user_id).first()

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}','{self.image_file}','{self.role}')" 
    

    # def get_email(self, email):
    #     return self.filter(self.get.email == email).first()

 
# class Post(db.Document):
#     title = db.StringField(max_length=150,required=True)
#     date_posted = db.DateTimeField(default = datetime.utcnow())
#     content = db.StringField()  
#     image_file = db.StringField(max_length=50,required=True,default='post.jpg')
#     author = db.ReferenceField(User,required=True)

#     def __repr__(self):
#         return f"Post('{self.title}','{self.date_posted}','{self.content}')"

def CreateRespone():
    answer={
        "status":False,
        "payload":{},
        "message":""
    } 
    return answer

def Respone(status, payload, message):
    answer = CreateRespone()
    answer['status']= status
    answer['payload']= payload
    answer['message']= message
    return answer

class DataTrain(db.Document):
    # query_class = UserModel
    # id = db.StringField(required=True, primary_key=True)
    author = db.StringField(max_length=100,required=True,default='page') 
    title = db.StringField(required=True,default='title')
    description = db.StringField(required=True,default='description')
    # image_file = db.StringField(max_length=50,required=True,default='avatar.png') 
    image_author = db.StringField(required=True,default='avatar.png') 
    url_page = db.StringField(required=True,default='url_page')
    url_image = db.StringField(required=True,default='url_image') 
    # date_posted = db.DateTimeField(default = datetime.utcnow())
    date_posted = db.StringField(max_length=50,required=True,default='date_posted')
    kind = db.StringField(max_length=100,required=True,default='kind') 
    like = db.StringField(max_length=50,required=True,default='like') 
    brand = db.StringField(required=True,default='brand') 
    tags = db.ListField(db.StringField(max_length=30))
    age_data = db.StringField(required=True,default='age_data') 
    view = db.StringField(required=True,default='view') 
    currency = db.StringField(required=True,default='currency') 
    price = db.StringField(required=True,default='price') 

    def to_json(self):
        return {
            "_id": str(self.id),
            "author": self.author,
            "title": self.title,
            "description": self.description,
            # "image_file": self.image_file,
            "image_author": self.image_author,
            "url_page": self.url_page,
            "kind": self.kind,
            "like": self.like,
            "brand": self.brand,
            "tags": self.tags
        }

    def __repr__(self):
        return f"DataTrain('{self.title}','{self.author}','{self.description}')"