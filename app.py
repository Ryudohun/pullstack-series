from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from email_utils import mail, send_schedule_email
from forms import RegistrationForm, LoginForm, ScheduleForm
from models import db, User, Schedule
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 이메일 설정
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_app_password'

# 초기화
db.init_app(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)  # 자동 로그인
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('로그인 성공!')
            return redirect(url_for('index'))
        else:
            flash('이메일 또는 비밀번호가 잘못되었습니다.')
    return render_template('login.html', form=form)

# 로그아웃
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 되었습니다.')
    return redirect(url_for('index'))

# 일정 추가
@app.route('/add_schedule', methods=['GET', 'POST'])
@login_required
def add_schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule = Schedule(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            time=form.time.data,
            user_id=current_user.id
        )
        db.session.add(schedule)
        db.session.commit()

        # 이메일 전송
        send_schedule_email(
            current_user.email,
            schedule.title,
            schedule.date,
            schedule.time,
            schedule.description
        )

        flash('일정이 등록되었습니다.')
        return redirect(url_for('index'))
    return render_template('add_schedule.html', form=form)

# 일정 조회
@app.route('/calendar')
@login_required
def calendar():
    schedules = Schedule.query.filter_by(user_id=current_user.id).all()
    return render_template('calendar.html', schedules=schedules)

# 실행
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
