from flask_mail import Mail, Message

mail = Mail()

def send_schedule_email(recipient, schedule):
    msg = Message(f"[일정 알림] {schedule.title}",
                recipients=[recipient])
    msg.body = f"내용: {schedule.description}\n날짜: {schedule.date} {schedule.time}"
    mail.send(msg)
