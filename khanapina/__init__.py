from flask import Flask, session
from flask_login import user_logged_in
from .models import Users, Recipies
from .utils import configutils, dbutils, authutils
from .views import auth, home, recipie

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    configutils.configure_app(app, test_config)
    authutils.init_login_manager(app)
    dbutils.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(recipie.bp)

    
    return app
