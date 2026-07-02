from extensions import db


class Department(db.Model):
    __tablename__ = 'departments'

    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(150), nullable=False)
    dept_head = db.Column(db.String(100))
    annual_budget = db.Column(db.Numeric(12, 2))
    courses = db.relationship('Course', back_populates='dept', lazy='dynamic')
    students = db.relationship('Student', back_populates='dept', lazy='dynamic')

    def to_dict(self):
        return {
            'dept_id': self.dept_id,
            'dept_name': self.dept_name,
            'dept_head': self.dept_head,
            'annual_budget': float(self.annual_budget or 0),
        }


class Course(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(200), nullable=False)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    credit_hrs = db.Column(db.Integer, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.dept_id'), nullable=False)
    dept = db.relationship('Department', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course', lazy='dynamic')

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_title': self.course_title,
            'course_code': self.course_code,
            'credit_hrs': self.credit_hrs,
            'dept_id': self.dept_id,
        }


class Student(db.Model):
    __tablename__ = 'students'

    stu_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    email_addr = db.Column(db.String(120), unique=True, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.dept_id'))
    join_year = db.Column(db.Integer)
    dept = db.relationship('Department', back_populates='students')
    enrollments = db.relationship('Enrollment', back_populates='student', lazy='dynamic')

    def to_dict(self):
        return {
            'stu_id': self.stu_id,
            'fname': self.fname,
            'lname': self.lname,
            'email_addr': self.email_addr,
            'join_year': self.join_year,
        }


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    __table_args__ = (db.UniqueConstraint('stu_id', 'course_id', name='uq_stu_course'),)

    enroll_id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.Integer, db.ForeignKey('students.stu_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    enrolled_on = db.Column(db.Date, nullable=False)
    grade_val = db.Column(db.String(5))
    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

    def to_dict(self):
        return {
            'enroll_id': self.enroll_id,
            'stu_id': self.stu_id,
            'course_id': self.course_id,
            'enrolled_on': str(self.enrolled_on),
            'grade_val': self.grade_val,
        }
