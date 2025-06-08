from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# 회원가입 폼
class RegistrationForm(FlaskForm):
    username = StringField('사용자 이름', validators=[
        DataRequired(message='사용자 이름을 입력해주세요.'),
        Length(min=2, max=20, message='이름은 2자 이상 20자 이하로 입력해주세요.')
    ])
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요.'),
        Email(message='올바른 이메일 형식을 입력해주세요.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요.'),
        Length(min=6, message='비밀번호는 최소 6자 이상이어야 합니다.')
    ])
    confirm_password = PasswordField('비밀번호 확인', validators=[
        DataRequired(message='비밀번호 확인을 입력해주세요.'),
        EqualTo('password', message='비밀번호가 일치하지 않습니다.')
    ])
    submit = SubmitField('회원가입')

# 로그인 폼
class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요.'),
        Email(message='올바른 이메일 형식을 입력해주세요.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요.')
    ])
    submit = SubmitField('로그인')

# 일정 추가 폼
class ScheduleForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired(message='제목을 입력해주세요.')])
    description = TextAreaField('설명')
    date = DateField('날짜', format='%Y-%m-%d', validators=[
        DataRequired(message='날짜를 입력해주세요. (예: 2025-06-08)')
    ])
    time = TimeField('시간', format='%H:%M', validators=[
        DataRequired(message='시간을 입력해주세요. (예: 14:00)')
    ])
    submit = SubmitField('일정 추가')
