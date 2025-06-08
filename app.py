from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Schedule
from forms import LoginForm, RegisterForm, ScheduleForm
from email_utils import send_schedule_email
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedules.db'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def index():
    schedules = Schedule.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', schedules=schedules)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('회원가입 완료! 로그인해주세요.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('로그인 실패. 아이디/비밀번호 확인하세요.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule = Schedule(
            user_id=current_user.id,
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            description=form.description.data
        )
        db.session.add(schedule)
        db.session.commit()
        send_schedule_email(current_user.email, schedule)
        return redirect(url_for('index'))
    return render_template('add_schedule.html', form=form)

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)
