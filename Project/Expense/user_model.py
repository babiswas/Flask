from werkzeug.security import check_password_hash
from datetime import datetime
from config import db

class User(db.Model):
   __tablename__="users"
   id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
   name=db.Column(db.String(100),nullable=False)
   username=db.Column(db.String(100),nullable=False,unique=True)
   email=db.Column(db.String(200),nullable=False,unique=True)
   password=db.Column(db.String(200))
   created_on=db.Column(db.DateTime(),default=datetime.utcnow())
   expense=db.relationship('Expense',backref='owner')

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