from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('회원가입')

class LoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

class ScheduleForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired()])
    description = TextAreaField('내용', validators=[DataRequired()])
    date = DateField('날짜', validators=[DataRequired()])
    time = TimeField('시간', validators=[DataRequired()])
    submit = SubmitField('일정 추가')
