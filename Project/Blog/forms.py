from wtforms import Form,StringField,PasswordField,IntegerField,TextAreaField

class RegisterForm(Form):
    name=StringField("Enter your name")
    username=StringField("Enter Username")
    email=StringField("Enter email")
    password=PasswordField("Enter Password")
    confirm=PasswordField("Confirm Password")

class LoginForm(Form):
    email=StringField("Email")
    password=PasswordField("Password")

class PostForm(Form):
   title=StringField("Title")
   content=TextAreaField("Content")
   