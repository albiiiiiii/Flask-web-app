from flask import flash,request
from models import User
from __init__ import db
#the werkzeug module is used to store passwords more securely (by hashing it and not just by plain text)
from werkzeug.security import generate_password_hash,check_password_hash

#function to check if sign up credentials are properly entered
def authenticatesignup(email,pw,firstname):
    if request.method=="POST":
        user=User.query.filter_by(email=email).first()
        if(user):
            flash('Email already exists, Sign in using a different email!')
            return False
        elif (email=='' or pw=='' or firstname==''):
            flash('Email/Password/Name field cannot be empty!')
            return False
        elif (len(pw)<=4):
            flash('Password must be more than 4 characters!')
            return False
        elif (firstname in '0123456789'):
            flash('Name cannot contain numerical values!')
            return False
        else:
            #scrypt is used to encrypt the password for an added layer of security for users
            new_user=User(email=email,firstname=firstname,password=generate_password_hash(pw,method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            return True
        
#function to check if login credentials are properly entered        
def authenticatelogin(email,pw):
    if request.method=="POST":
        if (email=='' or pw==''):
            flash('Email/Password field cannot be empty!')
            return False
        if (len(pw)<=4):
            flash('Password must be more than 4 characters!')
            return False
        else:
            user=User.query.filter_by(email=email).first()
            if user:
                if(check_password_hash(user.password,pw)==True):
                    return True
                else:
                    flash('Invalid Password!')
                    return False
            else:
                flash('Email not found!')
                return False