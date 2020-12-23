from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request 
from flask import jsonify



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:36network@localhost/app3user'
db=SQLAlchemy(app)


user_usergroup=db.Table('user_usergroup',db.Column('user_id',db.Integer,db.ForeignKey('users.id')),db.Column('usergroup_id',db.Integer,db.ForeignKey('usergroups.id')))


class User(db.Model):
   __tablename__='users'
   id=db.Column(db.Integer,primary_key=True,autoincrement=True)
   username=db.Column(db.String(200),unique=True)
   email=db.Column(db.String(200),unique=True)
   firstname=db.Column(db.String(200))
   lastname=db.Column(db.String(200))
   group=db.relationship('Usergroup',secondary=user_usergroup,backref=db.backref('addgroup',lazy='dynamic'))
   
   def __init__(self,username,email,firstname,lastname):
       self.firstname=firstname
       self.lastname=lastname
       self.email=email
       self.username=username

   def __str__(self):
       return f"{self.username}"


class Usergroup(db.Model):
     __tablename__='usergroups'
     id=db.Column(db.Integer,primary_key=True)
     groupname=db.Column(db.String(200))
     description=db.Column(db.String(200))
     
          
     def __init__(self,groupname,description):
         self.groupname=groupname
         self.description=description

     def __str__(self):
         return f"{self.groupname}"



@app.route('/user',methods=['POST'])
def create_user():
   group=Usergroup.query.get(1)	
   user=request.get_json()
   newuser=User(username=user["username"],email=user["email"],firstname=user["firstname"],lastname=user["lastname"])
   group.addgroup.append(newuser)
   db.session.add(newuser)
   db.session.commit()
   return jsonify(user)


@app.route('/usergroup',methods=['POST'])
def create_usergroup():
   group=request.get_json()
   usergroup=Usergroup(groupname=group["groupname"],description=group["description"])
   db.session.add(usergroup)
   db.session.commit()
   return jsonify(group)


@app.route('/user/<int:userid>/usergroup/<int:usergroupid>',methods=['POST'])
def add_users_group(userid,usergroupid):
    group=Usergroup.query.get(usergroupid)
    user=User.query.get(userid)
    group.addgroup.append(user)
    db.session.commit()
    return jsonify({"created":True})
    

if __name__=="__main__":
   db.create_all()
   app.run(debug=True)

