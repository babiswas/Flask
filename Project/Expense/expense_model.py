from user_model import User
from config import db
from datetime import datetime

class Expense(db.Model):
   __tablename__="expense"
   id=db.Column(db.Integer,primary_key=True,autoincrement=True)
   item=db.Column(db.String(100),nullable=False)
   quantity=db.Column(db.Integer,nullable=False)
   date=db.Column(db.DateTime(),default=datetime.utcnow())
   price=db.Column(db.Integer,nullable=False,default=0)
   owner_id=db.Column(db.Integer,db.ForeignKey('users.id'))

   def __init__(self,item,quantity,price):
       self.item=item
       self.quantity=quantity
       self.price=price
       self.date=datetime.utcnow()

   def __str__(self):
       return f"{self.item} and {self.date}"
   
   