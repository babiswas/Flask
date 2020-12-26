from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm
from forms import LoginForm
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from functools import wraps

app=Flask(__name__)
app.config['SECRET_KEY']='I am Bapan'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:36network@localhost/grocery'
db=SQLAlchemy(app)




class User(db.Model):
   __tablename__="users"
   id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
   name=db.Column(db.String(100),nullable=False)
   username=db.Column(db.String(100),nullable=False,unique=True)
   email=db.Column(db.String(200),nullable=False,unique=True)
   password=db.Column(db.String(200))
   created_on=db.Column(db.DateTime(),default=datetime.utcnow())

   def __init__(self,name,username,email,password):
       self.name=name
       self.username=username
       self.email=email
       self.password=password
       self.created_on=datetime.utcnow()

   def check_password(self,password):
       return self.check_password_hash(self.password,password)

   def __repr__(self):
       return f"{self.username}"
   
  
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


def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
      try:
         if session['logged_in']:
            return f(*args,**kwargs)
         else:
           return redirect(url_for('login'))
      except Exception as e:
        return redirect(url_for('login'))
    return wrapper
        


@app.route('/index')
@login_required
def index():
  return render_template("index.html")


if __name__=="__main__":
   db.create_all()
   app.run(debug=True)