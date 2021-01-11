from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __reper__(self):
        return '<Task %r>' %self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    print(request.method)
    if request.method == 'POST':
        task_content = request.form['content']
        print("task_content", task_content)
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue add your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        print(tasks)
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    print("task_to", task_to_delete)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
