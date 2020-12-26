from config import app
from config import db
from user_views import *
from expense_views import *



if __name__=="__main__":
   db.create_all()
   app.run(debug=True)