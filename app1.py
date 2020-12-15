from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:36network@localhost/myappuser'
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='appuser'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True)
    email=db.Column(db.String(20),unique=True)

    def __init__(self,username,email):
        self.username=username
        self.email=email

    def __repr__(self):
        return f"{self.username}"



@app.route('/users',methods=['GET'])
def getusers():
   users=User.query.all()
   output=[]
   for user in users:
       currentuser={}
       currentuser['id']=user.id
       currentuser['email']=user.email
       currentuser['username']=user.username
       output.append(currentuser)
   return jsonify(output)

@app.route('/user',methods=['POST'])
def createuser():
   userdata=request.get_json()
   user=User(username=userdata['username'],email=userdata['email'])
   db.session.add(user)
   db.session.commit()
   return jsonify(userdata)

@app.route("/user/<int:index>")
def getuser(index):
    user=User.query.get(index)
    currentuser={}
    currentuser['id']=user.id
    currentuser['email']=user.email
    currentuser['username']=user.username
    return jsonify(currentuser)
   
   
if __name__=="__main__":
   app.run()


