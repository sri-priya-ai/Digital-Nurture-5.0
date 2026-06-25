# Python Backend Frameworks — Digital Nurture 5.0

## How to run each hands-on

### Hands-On 1, 2, 3 (Django)
```bash
cd handson_0X/coursemanager
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

### Hands-On 4 (Flask)
```bash
cd handson_04/flask_coursemanager
pip install -r ../requirements.txt
python app.py
```

### Hands-On 5 (Flask + SQLAlchemy)
```bash
cd handson_05/flask_coursemanager
pip install -r ../requirements.txt
flask db init && flask db migrate -m "initial" && flask db upgrade
python app.py
```

### Hands-On 6, 7 (FastAPI)
```bash
cd handson_0X/fastapi_coursemanager
pip install -r ../requirements.txt
uvicorn main:app --reload
# Docs at http://127.0.0.1:8000/docs
```

### Hands-On 8, 9 (Django — advanced)
```bash
cd handson_0X/coursemanager
pip install -r ../requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Hands-On 10 (Microservices)
```bash
# 3 terminals:
cd handson_10/course_service  && python app.py   # port 5001
cd handson_10/student_service && python app.py   # port 5002
cd handson_10/gateway         && python app.py   # port 5000
```
