from flask import session
from functools import wraps
from flask import redirect
from flask import url_for



def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
      try:
         if session['logged_in']:
            return f(*args,**kwargs)
         else:
           return redirect(url_for('login'))
      except Exception as e:
        return redirect(url_for('login'))
    return wrapper