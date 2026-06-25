# models.py — SQLAlchemy models for the Course Management system.
# Each class is a Python representation of a database table.
# Relationships let us navigate between tables using dot notation
# instead of writing raw JOIN queries by hand.

from app import db


class Department(db.Model):
    __tablename__ = 'department'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(120), nullable=False)
    head_of_dept = db.Column(db.String(120))
    budget       = db.Column(db.Numeric(12, 2), default=0)

    # back_populates links both ends of the relationship
    courses  = db.relationship('Course',  back_populates='department', lazy='dynamic')
    students = db.relationship('Student', back_populates='department', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name,
                'head_of_dept': self.head_of_dept, 'budget': float(self.budget)}


class Course(db.Model):
    __tablename__ = 'course'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(200), nullable=False)
    code          = db.Column(db.String(20), unique=True, nullable=False)
    credits       = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    department  = db.relationship('Department', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course', lazy='dynamic')

    def to_dict(self):
        # to_dict() is Flask's equivalent of a DRF serializer — converts the
        # ORM object into a plain dict that jsonify() can serialise
        return {
            'id': self.id, 'name': self.name,
            'code': self.code, 'credits': self.credits,
            'department_id': self.department_id,
        }


class Student(db.Model):
    __tablename__ = 'student'

    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(80), nullable=False)
    last_name       = db.Column(db.String(80), nullable=False)
    email           = db.Column(db.String(200), unique=True, nullable=False)
    department_id   = db.Column(db.Integer, db.ForeignKey('department.id'))
    enrollment_year = db.Column(db.Integer)

    department  = db.relationship('Department', back_populates='students')
    enrollments = db.relationship('Enrollment', back_populates='student', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id, 'first_name': self.first_name,
            'last_name': self.last_name, 'email': self.email,
            'department_id': self.department_id,
            'enrollment_year': self.enrollment_year,
        }


class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id       = db.Column(db.Integer, db.ForeignKey('course.id'),  nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    grade           = db.Column(db.String(5), nullable=True)

    student = db.relationship('Student', back_populates='enrollments')
    course  = db.relationship('Course',  back_populates='enrollments')

    # Prevents the same student from being enrolled in the same course twice
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id'),)

    def to_dict(self):
        return {
            'id': self.id, 'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': str(self.enrollment_date),
            'grade': self.grade,
        }
