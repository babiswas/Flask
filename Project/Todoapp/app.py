from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import url_for
from datetime import datetime
from flask import request
from flask import redirect


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:36network@localhost/employee1'
db=SQLAlchemy(app)


class Todo(db.Model):
	__tablename__='todo'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	content=db.Column(db.String(200),nullable=False)
	completed=db.Column(db.Integer,default=0)
	date_created=db.Column(db.DateTime,default=datetime.utcnow())

	def __init__(self,content,date_created=datetime.utcnow(),completed=0):
		self.content=content
		self.date_created=date_created
		self.completed=completed
		



@app.route("/",methods=['GET','POST'])
def index():
	if request.method=='POST':
			task_content=request.form['content']
			new_task=Todo(task_content)
			db.session.add(new_task)
			db.session.commit()
			return redirect(url_for("index"))
	else:
		tasks=Todo.query.order_by(Todo.date_created).all()
		return render_template("index.html",tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
	task_to_delete=Todo.query.get_or_404(id)
	try:
	   db.session.delete(task_to_delete)
	   db.session.commit()
	   return redirect("/")
	except:
		return "There was a problem deleting our task"


@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
	task=Todo.query.get_or_404(id)
	if request.method=="POST":
		task.content=request.form['content']
		try:
			db.session.commit()
			return redirect('/')
		except Exception as e:
			return "There is an issue updating your task"
	else:
		return render_template('update.html',task=task)


if __name__=="__main__":
   app.run(debug=True)
