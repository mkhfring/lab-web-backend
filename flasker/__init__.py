import os
import functools

from flask import Flask
from flask_jwt_extended import JWTManager
from sqlalchemy_media import StoreManager, FileSystemStore
from flask_cors import CORS

from .views import auth, member, fake_api, news
from .cli import init_app
from .models.db import ma



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
#        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    jwt = JWTManager()
    jwt.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    init_app(app)
    ma.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(member.member)
    app.register_blueprint(fake_api.fake)
    app.register_blueprint(news.news)
    

    return app
