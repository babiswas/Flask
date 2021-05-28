from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask import redirect,render_template,url_for,session,request
from form import AccountForm,RegisterForm,UserForm,GroupForm,LoginForm,UserUpdateForm

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:36network@localhost/app2'
app.config['SECRET_KEY']="I am Bapan"
db=SQLAlchemy(app)



group=db.Table('groups',db.Column('user_id',db.Integer,db.ForeignKey('users.id')),db.Column('group_id',db.Integer,db.ForeignKey('usergroups.id')))


class Account(db.Model):
        __tablename__='accounts'
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        name=db.Column(db.String(200),nullable=False)
        email=db.Column(db.String(200),unique=True)
        owner=db.relationship('User',backref='owner')
        admin_owner=db.relationship('Admin',backref='admin_owner')
        alluser_owner=db.relationship('AllUser',backref='alluser_role')
        account_group=db.relationship('UserGroup',backref='account_group')

        def __init__(self,name,email):
            self.name=name
            self.email=email


        def __str__(self):
            return f"{self.name}"



class User(db.Model):
        __tablename__='users'
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        username=db.Column(db.String(200),unique=True)
        email=db.Column(db.String(200),nullable=False)
        firstname=db.Column(db.String(200),nullable=False)
        lastname=db.Column(db.String(200),nullable=False)
        password=db.Column(db.String(200))
        is_active=db.Column(db.Boolean,nullable=False)
        owner_id=db.Column(db.Integer,db.ForeignKey('accounts.id'))
        mygroup=db.relationship('UserGroup',secondary=group,backref=db.backref('addgroup',lazy='dynamic'))

        
        def __init__(self,username,email,firstname,lastname,password,accountId,is_active):
            self.firstname=firstname
            self.lastname=lastname
            self.email=email
            self.username=username
            self.password=generate_password_hash(password)
            self.owner_id=accountId
            self.is_active=is_active

        def check_password(self,password):
            return check_password_hash(self.password,password)

        def __str__(self):
            return f"{self.username}"


class UserGroup(db.Model):
        __tablename__="usergroups"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        groupname=db.Column(db.String(200),nullable=False)
        description=db.Column(db.String(200))
        group_id=db.Column(db.Integer,db.ForeignKey('accounts.id'))


        def __init__(self,groupname,description,accountId):
            self.groupname=groupname
            self.description=description
            self.group_id=accountId

        def __str__(self):
            return f"{self.description}"


class Admin(db.Model):
        __tablename__="adminrole"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        userid=db.Column(db.Integer,nullable=False)
        is_admin=db.Column(db.Boolean,nullable=False)
        account_id=db.Column(db.Integer,db.ForeignKey('accounts.id'))

        def __init__(self,userid,is_admin,accountId):
            self.userid=userid
            self.is_admin=is_admin
            self.account_id=accountId

        def __str__(self):
            return f"{self.userid} admin role"


class AllUser(db.Model):
        __tablename__="alluser"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        userid=db.Column(db.Integer,nullable=False)
        is_user=db.Column(db.Boolean,nullable=False)
        account_id=db.Column(db.Integer,db.ForeignKey('accounts.id'))

        def __init__(self,userid,is_user,accountId):
            self.userid=userid
            self.is_user=is_user
            self.account_id=accountId

        def __str__(self):
            return f"{self.userid} user role"


@app.route('/account',methods=['GET','POST'])
def create_account():
    try:
        form=AccountForm(request.form)
        if request.method=='POST' and form.validate:
            name=request.form["name"]
            email=request.form["email"]
            account=Account(name,email)
            db.session.add(account)
            db.session.commit()
            admin=UserGroup('Admin','All admin group',account.id)
            user=UserGroup('All User','All user group',account.id)
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('add_root',accountId=account.id))
        return render_template('account.html',form=form)
    except Exception as e:
        print(e)



@app.route('/root/<int:accountId>',methods=["GET","POST"])
def add_root(accountId):
    form=RegisterForm(request.form)
    account=Account.query.get(accountId)
    if request.method=="POST" and form.validate:
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        username=request.form["username"]
        email=account.email
        password=request.form["password"]
        user=User(username,email,firstname,lastname,password,account.id,True)
        db.session.add(user)
        db.session.commit()
        admin=UserGroup.query.filter_by(groupname='Admin').filter_by(group_id=account.id).first()
        alluser=UserGroup.query.filter_by(groupname='All User').filter_by(group_id=account.id).first()
        admin.addgroup.append(user)
        alluser.addgroup.append(user)
        alladmin=Admin(user.id,True,account.id)
        all_user=AllUser(user.id,True,account.id)
        db.session.add(alladmin)
        db.session.add(all_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("root.html",form=form,email=account.email)


@app.route('/addUser',methods=["GET","POST"])
def add_user():
    admin=Admin.query.filter_by(userid=session["userid"]).first()
    if admin.is_admin==True:
        form=UserForm(request.form)
        if request.method=="POST" and form.validate:
            email=request.form["email"]
            password='XX'
            firstname=request.form["firstname"]
            lastname=request.form["lastname"]
            user=User(firstname,email,firstname,lastname,password,session["accountId"],False)
            db.session.add(user)
            db.session.commit()
            all_user=AllUser(user.id,True,user.owner_id)
            all_admin=Admin(user.id,False,user.owner_id)
            alluser=UserGroup.query.filter_by(groupname='All User').filter_by(group_id=user.owner_id).first()
            alluser.addgroup.append(user)
            db.session.add(all_user)
            db.session.add(alluser)
            db.session.add(all_admin)
            db.session.commit()
            return redirect(url_for('admin_home'))
        return render_template('create_user.html',form=form)
    else:
        return "Unauthorized!"


@app.route('/addGroup',methods=["GET","POST"])
def add_group():
    admin=Admin.query.filter_by(userid=session["userid"]).first()   
    if admin.is_admin==True:
        form=GroupForm(request.form)
        if request.method=="POST" and form.validate:
            groupname=request.form["groupname"]
            description=request.form["description"]
            group=UserGroup(groupname,description,session["accountId"])
            db.session.add(group)
            db.session.commit()
            return redirect(url_for('admin_home'))
        return render_template('create_group.html',form=form)


@app.route('/adminHome',methods=["GET"])
def admin_home():
    admin=Admin.query.filter_by(userid=session["userid"]).first()
    if admin.is_admin==True:
       all_user=User.query.filter_by(owner_id=session["accountId"])
       all_groups=UserGroup.query.filter_by(group_id=session["accountId"])
       return render_template('admin_home.html',users=all_user,groups=all_groups)


@app.route('/login',methods=["GET","POST"])
def login():
        form=LoginForm(request.form)
        if request.method=="POST" and form.validate:
           username=request.form["username"]
           password=request.form["password"]
           user=User.query.filter_by(username=username).first()
           if user:
                if check_password_hash(user.password,password):
                    if not user.is_active:
                        return redirect(url_for('edit_user',userid=user.id))
                    else:   
                        admin=Admin.query.filter_by(userid=user.id).first()
                        alluser=AllUser.query.filter_by(userid=user.id).first()
                        if admin.is_admin==True:
                            session["is_admin"]=True
                        else:
                            session["is_admin"]=False
                        if alluser.is_user==True:
                            session["is_user"]=True
                        else:
                            session["is_user"]=False
                        session["accountId"]=user.owner_id
                        session["userid"]=user.id
                        session["logged_in"]=True
                        return redirect(url_for('home'))
                else:
                    return redirect(url_for('login'))
        return render_template('login.html',form=form)



@app.route('/home',methods=["GET"])
def home():
        permission=dict()
        user=User.query.get(session["userid"])
        usergroups=UserGroup.query.join(group).filter(group.c.group_id==UserGroup.id).filter(UserGroup.group_id==user.owner_id).filter(group.c.user_id==user.id).all()
        if session["is_admin"]==True:
            permission["is_admin"]=True
        else:
            permission["is_admin"]=False
        if session["is_user"]==True:
            permission["is_user"]=True
        else:
            permission["is_user"]=False
        return render_template("user_home.html",groups=usergroups,user=user,permission=permission)


@app.route('/updateUser/<int:userid>',methods=['GET','POST'])
def edit_user(userid):
        user=User.query.filter_by(id=userid).first()
        print(user)
        userform=UserUpdateForm(obj=user)
        if request.method=="POST" and userform.validate:
            username=request.form["username"]
            password=request.form["password"]
            user.username=username
            user.password=generate_password_hash(password)
            user.is_active=True
            db.session.commit()
            return redirect(url_for('login'))
        return render_template("update_user.html",form=userform)


@app.route('/usergroup/<int:group_id>/users',methods=["GET"])
def get_users_group(group_id):
        admin=Admin.query.filter_by(userid=session["userid"]).first()
        if admin.is_admin==True:
            group=UserGroup.query.get(group_id)
            return render_template('groupusers.html',users=group.addgroup,group=group)
        else:
            return "Unauthorized"


@app.route('/logout',methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('login'))


    
if __name__=="__main__":
   db.create_all()
   app.run(debug=True)