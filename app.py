from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from email_utils import mail, send_schedule_email
from forms import RegistrationForm, LoginForm, ScheduleForm
from models import db, User, Schedule
from flask_wtf import CSRFProtect

mail = Mail()

app = Flask(__name__)

# 🔐 앱 설정
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 📧 이메일 설정
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # 본인 이메일
app.config['MAIL_PASSWORD'] = 'your_app_password'  # 앱 비밀번호 (웹메일 비번 아님!)

# 📦 확장 기능 초기화
db.init_app(app)
mail.init_app(app)
csrf = CSRFProtect(app)

# 🔐 로그인 관리자 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 페이지로 리디렉션 설정


# 🔁 사용자 로딩
@login_manager.user_loader
def load_user(user_id):
    if not user_id or not user_id.isdigit():
        return None
    return User.query.get(int(user_id))


# 🏠 홈
@app.route('/')
def index():
    # 로그인 상태를 확인
    if current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('login'))  # 로그인 안 된 상태면 로그인 페이지로 리디렉션


# 👤 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('회원가입이 완료되었습니다.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


# 🔓 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    flash('로그인 성공!', 'success')

                    # 로그인 후 이동할 페이지
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('calendar'))

            flash('이메일 또는 비밀번호가 잘못되었습니다.', 'danger')
        except Exception as e:
            flash('서버 오류가 발생했습니다.', 'danger')
    return render_template('login.html', form=form)


# 🔒 로그아웃
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('index'))


# 🗓️ 일정 추가
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

        # 📧 이메일 발송
        send_schedule_email(
            current_user.email,
            schedule.title,
            schedule.date,
            schedule.time,
            schedule.description
        )

        flash('일정이 등록되었습니다.', 'success')
        return redirect(url_for('calendar'))
    return render_template('add_schedule.html', form=form)


# 📅 일정 조회
@app.route('/calendar')
@login_required
def calendar():
    schedules = Schedule.query.filter_by(user_id=current_user.id).all()
    return render_template('calendar.html', schedules=schedules)


# 🛠️ 사용자 미리 등록하기 (앱 시작 시 실행)
def create_user():
    # 임의로 사용자 하나 생성 (이메일과 비밀번호 설정)
    user = User.query.filter_by(email='testuser@example.com').first()
    if not user:
        hashed_pw = generate_password_hash('testpassword123')  # 임의의 비밀번호
        new_user = User(username='testuser', email='testuser@example.com', password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        print("임의의 사용자 추가 완료")

        # testuser에 일정 추가
        test_user = User.query.filter_by(email='testuser@example.com').first()
        schedule = Schedule(
            title="테스트 일정",
            description="이 일정은 자동으로 생성되었습니다.",
            date="2025-06-10",  # 예시 날짜
            time="10:00",  # 예시 시간
            user_id=test_user.id
        )
        db.session.add(schedule)
        db.session.commit()
        print("임의의 일정 추가 완료")


# 🔄 앱 실행
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 데이터베이스가 없다면 생성
        create_user()  # 앱 시작 시 사용자 및 일정 추가
    app.run(debug=True)
