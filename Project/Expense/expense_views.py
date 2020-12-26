from flask import request
from config import app
from forms import ExpenseForm
from flask import session
from flask import url_for
from flask import redirect
from config import db
from user_model import User
from expense_model import Expense
from flask import render_template
from utility import login_required


@app.route('/expense/',methods=['GET','POST'])
@login_required
def create_expense():
   form=ExpenseForm(request.form)
   if request.method=='POST' and form.validate():
      email=session['email']
      user=User.query.filter_by(email=email).first()
      new_expense=Expense(form.item.data,form.quantity.data,form.price.data)
      new_expense.owner=user
      db.session.add(new_expense)
      db.session.commit()
      return redirect(url_for('expense_list'))
   else:
      return render_template('Expense.html',form=form)


@app.route('/expenselist/',methods=['GET'])
@login_required
def expense_list():
   expenses=Expense.query.all()
   return render_template('ExpenseList.html',expenses=expenses)












