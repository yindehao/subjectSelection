# _*_ coding: utf-8 _*_
"""
Time:     2022/10/9 13:56
Author:   Yin Dehao
Version:  V 1.0
File:     instructor_view.py
"""
from flask import Blueprint, render_template, session


from common.ext import db
from models import Instructor

bp = Blueprint("ibp", __name__, url_prefix='/instructor')


@bp.route('/')
def index():
    instructor_id = session['student_id']
    instructor = db.session.query(Instructor).filter_by(instructor_id=instructor_id).first()
    context = {'instructor_name': instructor.instructor_name}
    return render_template('instructor.html', **context)
