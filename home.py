#import flask module
from flask import render_template,url_for,redirect,request,session,flash
from auth import authenticatesignup,authenticatelogin
from __init__ import create_app,db
from models import User
from sqlalchemy import text
import sqlite3
app=create_app()

db_path = 'Model.db'

# Connect to the SQLite database
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#specifying the route for the homepage using a decorator
@app.route('/')
def home():   
    return render_template("home.html")

#methods are used to specify how information is sent (GET is public while POST is a secure method)
@app.route('/userlogin/',methods=['POST','GET'])
def userlogin():
    if request.method=='POST':
        if 'user' in session:
            flash('Already logged in!')
            user=User.query.filter_by(email=session['user']).first()
            return redirect(url_for('user',user=user.firstname,user_id=user.id))
        #request the email and password of the user from the form
        email1=request.form['email']
        pw=request.form['pw']
        if(authenticatelogin(email1,pw)==True):
            session['user']=email1
            #display a message showing successful login
            flash('Login Success!')
            user=User.query.filter_by(email=email1).first()
            return redirect(url_for('user',user=user.firstname,user_id=user.id))
        #creates a session variable stored until user logs out
        else:
            return redirect(url_for('userlogin'))
    else:
        if 'user' in session:
            flash('Already logged in!')
            u=User.query.filter_by(email=session['user']).first()
            user=u.firstname
            id=u.id
            return redirect(url_for('user',user=user,user_id=id))
        return render_template('userlogin.html')
    
#redirect for successful login/signup
@app.route('/user/<user>',methods=['POST','GET'])
def user(user):
    if request.method=="POST":
        note1=request.form['note']
        name=request.form['notename']
        if(len(note1)<1 or len(name)<1):
            flash('Note length/name should be greater than 1!')
        else:
            flash('Note has been saved!')
            user=User.query.filter_by(email=session['user']).first()
            id=user.id
            new_note=User(notename=name,note=note1)
            db.session.add(new_note)
            db.session.commit()

    #checks if user has already logged in and if a session is active
    if 'user' in session:
        return render_template('user.html',fn=user)
        
    else:
        #redirect back to user login page
        flash("You are not logged in!")
        return redirect(url_for('userlogin'))
    
#specifying the route for the admin page similarly
@app.route("/usersignup/",methods=['POST','GET'])
def usersignup():
    if 'user' in session:
        flash('Log out from the current session to sign up!')
        user=User.query.filter_by(email=session['user']).first()
        return redirect(url_for('user',user=user.firstname))
    else:
        if request.method=='POST':
            email=request.form['email']
            pw=request.form['pw']
            firstname=request.form['firstname']
            if(authenticatesignup(email,pw,firstname)==True):
                flash('Successfully signed in!')
                session['user']=email
                user=User.query.filter_by(email=session['user']).first()
                return redirect(url_for('user',user=user.firstname))
            else:
                return redirect(url_for('usersignup'))
        else:
            if 'user' in session:
                flash('Already logged in!')
                user=User.query.filter_by(email=session['user']).value(text(firstname))
                return redirect(url_for('user',user=user,user_id=user.user_id))
            return render_template('usersignup.html')
        
@app.route('/logout/')
def logout():
    session.pop('user',None)
    flash('Successfully logged out')
    return redirect(url_for('userlogin'))
        
@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/notes/')
def notes():
    mail=session['user']
    user=User.query.filter_by(email=mail).first()
    id=user.id
    if(User.query.filter_by(id=id)):
        b=User.note
    else:
        flash('No notes to display!')
        return redirect(url_for('user'))
    
@app.route('/view/')
def view():
    return render_template('view.html',values=User.query.all())

#clear the login session in the event of browser closure
def clear_session():
    session.clear()

#running the web server only if the file is run and not imported
if __name__=='__main__':
        app.run(debug=True)