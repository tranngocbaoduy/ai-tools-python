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
    image_file = db.StringField(max_length=50,required=True, default='avatar.png')
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
#     image_file = db.StringField(max_length=50,required=True, default='post.jpg')
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
    author = db.StringField(max_length=100,required=True, default='page') 
    title = db.StringField(required=True, default='title')
    description = db.StringField(required=True, default='description')
    # image_file = db.StringField(max_length=50,required=True, default='avatar.png') 
    image_author = db.StringField(required=True, default='avatar.png') 
    url_page = db.StringField(required=True, default='url_page')
    url_image = db.StringField(required=True, default='url_image') 
    # date_posted = db.DateTimeField(default = datetime.utcnow())
    date_posted = db.StringField(max_length=50,required=True, default='date_posted')
    kind = db.StringField(max_length=100,required=True, default='kind') 
    like = db.StringField(max_length=50,required=True, default='like') 
    brand = db.StringField(required=True, default='brand') 
    tags = db.ListField(db.StringField(max_length=30))
    age_data = db.StringField(required=True, default='age_data') 
    view = db.StringField(required=True, default='view') 
    currency = db.StringField(required=True, default='currency') 
    price = db.StringField(required=True, default='price') 

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

class AdditionalInfo(db.Document,JsonSerializable):
    city = db.StringField() 
    committee_id = db.StringField()  
    director_name = db.StringField() 
    email = db.StringField() 
    phone_number = db.StringField() 
    point_of_contact = db.StringField() 
    state = db.StringField() 
    street_address_1 = db.StringField() 
    street_address_2 = db.StringField() 
    treasurer_name = db.StringField() 
    website = db.StringField() 
    zipcode = db.StringField() 

class InfoAd(db.Document,JsonSerializable): 
    ad_creative_id = db.StringField(required=True, default='ad_creative_id') 
    additional_info = db.StringField(required=True, default='additional_info') 
    by_line = db.StringField(required=True, default='by_line') 
    caption = db.StringField(required=True, default='caption')  
    country_iso_code = db.StringField(required=True, default='caption') 
    creation_time = db.IntField(required=True, default='0')
    current_page_name = db.StringField(required=True, default='current_page_name')  
    original_image_url = db.StringField(required=True, default='original_image_url') 
    resize_image_url = db.StringField(required=True, default='resize_image_url') 
    instagram_actor_name = db.StringField(required=True, default='instagram_actor_name') 
    instagram_profile_pic_url = db.StringField(required=True, default='instagram_profile_pic_url')  
    link_description = db.StringField(required=True, default='link_description')  
    link_url = db.StringField(required=True, default='link_url')  
    page_categories  = db.StringField(required=True, default='page_categories')  
    page_id = db.StringField(required=True, default='page_id')  
    page_is_deleted = db.BooleanField(required=True, default=False)
    page_like_count = db.StringField(required=True, default='page_like_count')  
    page_name = db.StringField(required=True, default='page_name')  
    page_profile_picture_url = db.StringField(required=True, default='page_profile_picture_url')  
    page_profile_uri = db.StringField(required=True, default='page_profile_uri')   
    page_welcome_message = db.StringField()
    root_reshared_post = db.StringField()
    title = db.StringField(required=True, default='title')  
    version = db.StringField(required=True, default='version')   

class FBAdTrain(db.Document,JsonSerializable): 
    ad_id = db.StringField(required=True, default='adId') 
    ad_archive_id = db.StringField(required=True, default='ad_archiveID')  
    end_date= db.IntField(required=True, default=0)  
    start_date = db.IntField(required=True, default=0)  
    gated_type = db.StringField(required=True, default='gated_type')  
    is_active = db.BooleanField(required=True, default=False)  
    is_profile_page = db.BooleanField(required=True, default=False)  
    is_promoted_news= db.BooleanField(required=True, default=False)  
    page_id = db.StringField(required=True, default='pageID') 
    page_name = db.StringField(required=True, default='pageName')  
    snap_shot = db.StringField(required=True, default='snap_shot')
    tags = db.ListField(db.StringField(max_length=30))
    age_data = db.StringField(required=True, default='age_data') 
    view = db.StringField(required=True, default='view') 
    currency = db.StringField(required=True, default='currency') 
    price = db.StringField(required=True, default='price') 
    region_data = db.StringField(required=True, default='region_data') 
 

class DMMAdTrain(db.Document): 
    ad_id = db.StringField(required=True, default='adId')    
    number_of_like = db.IntField(required=True, default=0)
    number_of_comment = db.IntField(required=True, default=0)
    number_of_share = db.IntField(required=True, default=0) 
    is_active = db.BooleanField(required=True, default=True) 
    original_image_url = db.StringField(required=True, default='original_image_url') 
    page_id = db.StringField(required=True, default='pageID') 
    page_name = db.StringField(required=True, default='pageName')  
    link_url =  db.StringField(required=True, default='link_url')  

class DataTrain(db.Document): 
    author = db.StringField(max_length=100,required=True, default='page') 
    title = db.StringField(required=True, default='title')
    description = db.StringField(required=True, default='description')
    # image_file = db.StringField(max_length=50,required=True, default='avatar.png') 
    image_author = db.StringField(required=True, default='avatar.png') 
    url_page = db.StringField(required=True, default='url_page')
    url_image = db.StringField(required=True, default='url_image') 
    # date_posted = db.DateTimeField(default = datetime.utcnow())
    date_posted = db.StringField(max_length=50,required=True, default='date_posted')
    kind = db.StringField(max_length=100,required=True, default='kind') 
    like = db.StringField(max_length=50,required=True, default='like') 
    brand = db.StringField(required=True, default='brand') 
    tags = db.ListField(db.StringField(max_length=30))
    age_data = db.StringField(required=True, default='age_data') 
    view = db.StringField(required=True, default='view') 
    currency = db.StringField(required=True, default='currency') 
    price = db.StringField(required=True, default='price') 