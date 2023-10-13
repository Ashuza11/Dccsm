from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "cash.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hshhdjdkdkksjssjsj'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views 
    from .dccsm import dccsm

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(dccsm, url_prefix='/')

    from .models import Node, MemoryBloc,  Directory, CacheNode, MessageSimulation

    with app.app_context():
        create_database()

    return app

def create_database():
        if not path.exists('dccsm/' + DB_NAME):
            db.create_all()
            print('Created Database!')