from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.teacher import Teacher
from flask_app.models.assignment import Assignment
from flask_app.models import teacher


@app.route('/assignment/create')
def create():
    data={
        'id': session['user_id']
    }
    return render_template('create.html', teacher=Teacher.get_from_id(data))


@app.route('/create_assignment', methods=['POST'])
def create_assignment():
    if not Assignment.validate_assignment(request.form):
        return redirect('/assignment/create')
    data={
        'name':request.form['name'],
        'description':request.form['description'],
        'points':request.form['points'],
        'date':request.form['date'],
        'created_at': request.form['created_at'],
        'teacher_id':request.form['teacher_id']
    }
    Assignment.save_assignment(data)
    return redirect('/dashboard')

@app.route('/assignment/<int:teacher_id>/<int:id>')
def view_assignment(id,teacher_id):
    data={
        'id':id,
        'teacher_id':teacher_id
    }
    return render_template('view.html',assignment=Assignment.get_from_id(data), teacher=Teacher.get_from_teacher_id(data))

@app.route('/assignment/add_grades/<int:assignment_id>')
def add_grades(assignment_id):
    data={
        'id': assignment_id,
        'teacher_id': session['user_id']
    }
    return render_template('grade.html', teacher=Teacher.get_from_teacher_id(data),assignment=Assignment.get_from_id(data),teachers_students=Teacher.get_teachers_students(data))

@app.route('/assignment/<int:assignment_id>/save_grades', methods=['POST'])
def save_grades(assignment_id):
    data={
        'student_id': request.form['student_id'],
        'assignment_id':assignment_id,
        'grade':request.form['grade']
    }
    Assignment.save_grades(data)
    return redirect('/dashboard')