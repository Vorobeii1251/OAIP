from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(10), default="medium")
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def is_overdue(self):
        return not self.is_done and self.deadline < datetime.now()

    @property
    def is_today(self):
        if self.is_done:
            return False
        today = datetime.now().date()
        return self.deadline.date() == today

    @property
    def is_this_week(self):
        if self.is_done:
            return False
        now = datetime.now()
        today = now.date()
        if self.deadline.date() == today:
            return False
        end_of_week = today.fromordinal(today.toordinal() + 7)
        return today < self.deadline.date() <= end_of_week

    @property
    def is_later(self):
        if self.is_done:
            return False
        today = datetime.now().date()
        end_of_week = today.fromordinal(today.toordinal() + 7)
        return self.deadline.date() > end_of_week

    def __repr__(self):
        return f"<Task {self.id} {self.title!r}>"