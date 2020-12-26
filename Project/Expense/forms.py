from wtforms import Form,StringField,PasswordField,IntegerField

class RegisterForm(Form):
    name=StringField("Enter your name")
    username=StringField("Enter Username")
    email=StringField("Enter email")
    password=PasswordField("Enter Password")
    confirm=PasswordField("Confirm Password")

class LoginForm(Form):
    email=StringField("Email")
    password=PasswordField("Password")

class ExpenseForm(Form):
   item=StringField("Enter the item name")
   quantity=IntegerField("Enter the item quantity")
   price=IntegerField("Enter the price of the item")
   
    
    




