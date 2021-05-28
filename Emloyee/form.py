from wtforms import Form,StringField,PasswordField,IntegerField,TextAreaField

class AccountForm(Form):
        name=StringField("Account Name")
        email=StringField("Root User Mail")


class RegisterForm(Form):
        firstname=StringField("Firstname")
        lastname=StringField("Lastname")
        username=StringField("Username")
        password=StringField("Password")
        confirm=StringField("Confirm Password")


class UserForm(Form):
        email=StringField("Email")
        firstname=StringField("Firstname")
        lastname=StringField("Lastname")
        username=StringField("Username")


class GroupForm(Form):
        groupname=StringField("Usergroup Name")
        description=StringField("Group Description")


class LoginForm(Form):
    username=StringField("Username")
    password=StringField("Password")

class UserUpdateForm(Form):
    username=StringField("Username")
    password=StringField("password")





        
        
