from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm
from flask import request
from flask import url_for
from flask import redirect

app=Flask(__name__)
app.config['SECRET_KEY']='I am Bapan'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/grocery'
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
   
  

@app.route('/index')
def index():
  return render_template("index.html")


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


if __name__=="__main__":
   db.create_all()
   app.run(debug=True)
