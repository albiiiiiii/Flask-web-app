from __init__ import db

class User(db.Model):
    #giving each row a unique ID (primary key) which is an Integer
    id=db.Column(db.Integer,primary_key=True)
    #name and email column is created which accepts only strings
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    firstname=db.Column(db.String(100))