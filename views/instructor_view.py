# _*_ coding: utf-8 _*_
"""
Time:     2022/10/9 13:56
Author:   Yin Dehao
Version:  V 1.0
File:     instructor_view.py
"""
from flask import Blueprint, render_template, request, g, redirect, url_for, flash, session
# from decorators import login_required
# from .forms import QuestionForm,AnswerForm
# from models import QuestionModel,AnswerModel
from common.ext import db
from sqlalchemy import or_

from models import Instructor

bp = Blueprint("ibp", __name__, url_prefix='/instructor')


@bp.route('/')
def index():
    instructor_id = session['student_id']
    instructor = db.session.query(Instructor).filter_by(instructor_id=instructor_id).first()
    context = {'instructor_name': instructor.instructor_name}
    return render_template('instructor.html', **context)
