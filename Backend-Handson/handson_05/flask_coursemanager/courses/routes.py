from flask import Blueprint, jsonify, request
from extensions import db
from courses.models import Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


def ok(payload, code=200):
    return jsonify({'status': 'success', 'data': payload}), code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    rows = Course.query.all()
    return ok([r.to_dict() for r in rows])


@courses_bp.route('/', methods=['POST'])
def add_course():
    body = request.get_json()
    if not body:
        return jsonify({'error': 'JSON body required'}), 400

    missing = [f for f in ('course_title', 'course_code', 'credit_hrs', 'dept_id') if f not in body]
    if missing:
        return jsonify({'error': f"Missing: {', '.join(missing)}"}), 400

    entry = Course(
        course_title=body['course_title'],
        course_code=body['course_code'],
        credit_hrs=body['credit_hrs'],
        dept_id=body['dept_id'],
    )
    db.session.add(entry)
    db.session.commit()
    return ok(entry.to_dict(), 201)


@courses_bp.route('/<int:cid>/', methods=['GET'])
def fetch_course(cid):
    obj = Course.query.get_or_404(cid)
    return ok(obj.to_dict())


@courses_bp.route('/<int:cid>/', methods=['PUT'])
def update_course(cid):
    obj = Course.query.get_or_404(cid)
    body = request.get_json()
    if not body:
        return jsonify({'error': 'JSON body required'}), 400

    for fld in ('course_title', 'course_code', 'credit_hrs', 'dept_id'):
        if fld in body:
            setattr(obj, fld, body[fld])

    db.session.commit()
    return ok(obj.to_dict())


@courses_bp.route('/<int:cid>/', methods=['DELETE'])
def delete_course(cid):
    obj = Course.query.get_or_404(cid)
    db.session.delete(obj)
    db.session.commit()
    return '', 204


@courses_bp.route('/<int:cid>/students/', methods=['GET'])
def course_students(cid):
    Course.query.get_or_404(cid)
    rows = (
        db.session.query(Student)
        .join(Enrollment, Enrollment.stu_id == Student.stu_id)
        .filter(Enrollment.course_id == cid)
        .all()
    )
    return ok([s.to_dict() for s in rows])
