from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class TaskForm(FlaskForm):
    title = StringField(
        "Название",
        validators=[DataRequired(message="Название не может быть пустым"),
                    Length(max=200)],
    )
    description = TextAreaField("Описание")
    deadline = DateTimeLocalField(
        "Дедлайн",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired(message="Укажите дедлайн")],
    )
    priority = SelectField(
        "Приоритет",
        choices=[("low", "Низкий"), ("medium", "Средний"), ("high", "Высокий")],
        default="medium",
    )
    submit = SubmitField("Сохранить")

    def validate_deadline(self, field):
        if self.is_edit:
            return
        if field.data < datetime.now():
            raise ValidationError("Дедлайн не может быть в прошлом")

    is_edit = False