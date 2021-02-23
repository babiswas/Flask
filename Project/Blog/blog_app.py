from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime
from forms import RegisterForm,LoginForm,PostForm
from functools import wraps


app=Flask(__name__)
app.config['SECRET_KEY']="I am Bapan"
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:36network@localhost/blogapp'
db=SQLAlchemy(app)


def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
      try:
         if session['logged_in']:
            return f(*args,**kwargs)
         else:
            raise Exception
      except Exception as e:
        return redirect(url_for('login'))
    return wrapper


class Post(db.Model):
   __tablename__="posts"
   id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
   title=db.Column(db.String(100),nullable=False)
   content=db.Column(db.Text(),nullable=False)
   created_on=db.Column(db.DateTime(),default=datetime.utcnow())
   author=db.Column(db.Integer,db.ForeignKey('users.id'))

   def __init__(self,title,content,author):
       self.title=title
       self.content=content
       self.created_on=datetime.utcnow()
       self.author=author

   def __repr__(self):
       return f"{self.title}"


class User(db.Model):
   __tablename__="users"
   id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
   name=db.Column(db.String(100),nullable=False)
   username=db.Column(db.String(100),nullable=False,unique=True)
   email=db.Column(db.String(200),nullable=False,unique=True)
   password=db.Column(db.String(200))
   created_on=db.Column(db.DateTime(),default=datetime.utcnow())
   posts=db.relationship('Post',backref='owner')

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

@app.route('/addpost',methods=['GET','POST'])
@login_required
def add_post():
   form=PostForm(request.form)
   if request.method=='POST' and form.validate():
      email=session['email']
      author=User.query.filter_by(email=email).first()
      new_post=Post(form.title.data,form.content.data,author.id)
      db.session.add(new_post)
      db.session.commit()
      return redirect(url_for('post_list'))
   else:
      return render_template('post.html',form=form)


@app.route('/postlist',methods=['GET'])
@login_required
def post_list():
   page=request.args.get('page',1,type=int)
   user=User.query.filter_by(email=session['email']).first()
   posts=Post.query.filter_by(author=user.id).paginate(page,4,False)
   next_url=url_for('post_list',page=posts.next_num) if posts.has_next else None
   prev_url=url_for('post_list',page=posts.prev_num) if posts.has_prev else None
   return render_template('postlist.html',posts=posts.items,next_url=next_url,prev_url=prev_url)

@app.route('/register/',methods=['GET','POST'])
@login_required
def register():
   form=RegisterForm(request.form)
   if request.method=='POST' and form.validate():
      password=generate_password_hash(form.password.data,method='sha256')
      new_user=User(form.name.data,form.username.data,form.email.data,password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('login'))
   else:
      return render_template('register.html',form=form)


@app.route('/postdetails/<int:id>',methods=['GET'])
@login_required
def post_detail(id):
    post=Post.query.get(id)
    user=User.query.get(post.author)
    if user.email==session['email']:
       return render_template('post_detail.html',post=post)
    else:
       return "<h1>Unauthorized</h1>"
    
    
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
            return redirect(url_for('add_post'))
         else:
            return redirect(url_for('login'))
   return render_template('login.html',form=form)


@app.route('/postedit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
   post=Post.query.get(id)
   user=User.query.get(post.author)
   if user.email!=session['email']:
      return "<h1>Unauthorized</h1>"
   form=PostForm(obj=post)
   if request.method=="POST" and form.validate():
      post.title=request.form['title']
      post.content=request.form['content']
      db.session.commit()
      return redirect(url_for('post_detail',id=id))
   return render_template("post.html",form=form)

@app.route('/logout/')
def logout():
   session['logged_in']=False
   session.clear()
   return redirect(url_for('login'))




if __name__=="__main__":
   db.create_all()
   app.run(debug=True)