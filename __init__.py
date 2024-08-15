from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from datetime import timedelta

#created a database object
db=SQLAlchemy()
NAME='database.db'

def create_app():
    app=Flask(__name__)
    app.permanent_session_lifetime=timedelta(minutes=15)
    app.config['SECRET_KEY']='sfdeqdwfr'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{NAME}'
    #connect the database with the app
    db.init_app(app)
    create_database(app)
    return app

def create_database(app):
    if not path.exists('website/'+NAME):
        with app.app_context():
            db.create_all()
            print('database created!')
