from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
db = SQLAlchemy(app)


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, unique=True, nullable=False)
	date = db.Column(db.DateTime, default=datetime.now)

	def __repr__(self):
		return f'Todo({self.id} - {self.content} - {self.date})'

with app.app_context():
    db.create_all()


@app.route('/')
def home():
	todos = Todo.query.all()
	return render_template('home.html', todos=todos)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/<int:todo_id>')
def detail(todo_id):
	todo = Todo.query.get(todo_id)
	return render_template('detail.html', todo=todo)


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
	todo = Todo.query.get(todo_id)
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)