from flask import Flask
from flask_mongoengine import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from searchai.config import Config
# from flask_dance.contrib.twitter import make_twiiter_blueprint, twitter


db = MongoEngine() 
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger'
# twitter_blueprint = make_twiiter_blueprint(api_key='', api_secret='')

mail = Mail()
 
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config) 

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from searchai.users.routes import users 
    from searchai.dataset.routes import dataset 
    from searchai.main.routes import main 

    app.register_blueprint(users) 
    app.register_blueprint(main) 
    app.register_blueprint(dataset) 

    return app