from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, request

from models import db, Task
from forms import TaskForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tasks = Task.query.order_by(Task.deadline.asc()).all()

    overdue = [t for t in tasks if t.is_overdue]
    today = [t for t in tasks if t.is_today]
    this_week = [t for t in tasks if t.is_this_week]
    later = [t for t in tasks if t.is_later]
    done = [t for t in tasks if t.is_done]

    total = len(tasks)
    completed = len(done)

    return render_template(
        "index.html",
        overdue=overdue,
        today=today,
        this_week=this_week,
        later=later,
        done=done,
        total=total,
        completed=completed,
        form=TaskForm(),
    )


@app.route("/add", methods=["POST"])
def add():
    form = TaskForm()
    form.is_edit = False
    if form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=(form.description.data or "").strip(),
            deadline=form.deadline.data,
            priority=form.priority.data,
        )
        db.session.add(task)
        db.session.commit()
        flash("Задача добавлена", "success")
    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{field}: {err}", "danger")
    return redirect(url_for("index"))


@app.route("/task/<int:task_id>/toggle", methods=["POST"])
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/task/<int:task_id>/delete", methods=["POST"])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Задача удалена", "info")
    return redirect(url_for("index"))


@app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    form.is_edit = True

    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = (form.description.data or "").strip()
        task.deadline = form.deadline.data
        task.priority = form.priority.data
        db.session.commit()
        flash("Задача обновлена", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", form=form, task=task)


if __name__ == "__main__":
    app.run(debug=True)