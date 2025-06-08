import os
import zipfile

# 프로젝트 이름
project_name = "student_schedule_app"
os.makedirs(f"{project_name}/templates", exist_ok=True)
os.makedirs(f"{project_name}/static", exist_ok=True)

# 파일 내용 정의
files = {
    f"{project_name}/requirements.txt": """Flask
Flask-Login
Flask-WTF
email-validator
Flask-Mail
WTForms
""",
    f"{project_name}/app.py": "### 여기에 app.py 전체 코드 붙여 넣기 ###",
    f"{project_name}/models.py": "### 여기에 models.py 전체 코드 붙여 넣기 ###",
    f"{project_name}/forms.py": "### 여기에 forms.py 전체 코드 붙여 넣기 ###",
    f"{project_name}/email_utils.py": "### 여기에 email_utils.py 전체 코드 붙여 넣기 ###",
    f"{project_name}/templates/base.html": "<!DOCTYPE html><html><body>{% block content %}{% endblock %}</body></html>",
    f"{project_name}/templates/index.html": "### index.html 코드 입력 ###",
    f"{project_name}/templates/login.html": "### login.html 코드 입력 ###",
    f"{project_name}/templates/register.html": "### register.html 코드 입력 ###",
    f"{project_name}/templates/add_schedule.html": "### add_schedule.html 코드 입력 ###",
    f"{project_name}/templates/calendar.html": """<!DOCTYPE html>
<html>
<head>
    <link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/main.min.css' rel='stylesheet' />
    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/main.min.js'></script>
    <script>
      document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          events: '/api/schedules'
        });
        calendar.render();
      });
    </script>
</head>
<body>
  <h1>📅 캘린더 보기</h1>
  <div id='calendar'></div>
</body>
</html>
""",
    f"{project_name}/static/main.css": "/* 기본 CSS 스타일 */"
}

# 파일 생성
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 압축 파일 만들기
zip_filename = f"{project_name}.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, file_list in os.walk(project_name):
        for file in file_list:
            filepath = os.path.join(root, file)
            zipf.write(filepath, os.path.relpath(filepath, project_name))

print(f"{zip_filename} 생성 완료!")
