from flask import request
from config import app
from forms import  RegisterForm
from forms import  LoginForm
from flask import session
from flask import url_for
from flask import redirect
from config import db
from user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
from utility import login_required


@app.route('/register/',methods=['GET','POST'])
def register():
   form=RegisterForm(request.form)
   if request.method=='POST' and form.validate():
      password=generate_password_hash(form.password.data,method='sha256')
      new_user=User(form.name.data,form.username.data,form.email.data,password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('index'))
   else:
      return render_template('register.html',form=form)


@app.route('/login/',methods=['GET','POST'])
def login():
   form=LoginForm(request.form)
   if request.method=='POST' and form.validate:
      user=User.query.filter_by(email=form.email.data).first()
      if user:
         if check_password_hash(user.password,form.password.data):
            session['logged_in']=True
            session['email']=user.email
            session['username']=user.username
            return redirect(url_for('index'))
         else:
            return redirect(url_for('login'))
   return render_template('login.html',form=form)

@app.route('/logout/')
def logout():
   session['logged_in']=False
   return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
  return render_template("index.html")







