from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.teacher import Teacher
from flask_app.models.assignment import Assignment
from flask_app.models.student import Student
from flask_app.models.grade import Grade



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
        'teacher_id':request.form['teacher_id'],
    }
    Assignment.save_assignment(data)
    return redirect('/dashboard')

@app.route('/assignment/<int:id>')
def view_assignment(id):
    data={
        'id':session['user_id'],
        'assignment_id':id
    }
    return render_template('view.html',assignment=Assignment.get_from_id(data), teacher=Teacher.get_from_teacher_id(data))

@app.route('/assignment/add_grades/<int:assignment_id>')
def add_grades(assignment_id):
    data={
        'id': session['user_id'],
        'assignment_id': assignment_id
    }
    return render_template('grade.html', assignment=Assignment.get_from_id(data),teacher=Teacher.get_teachers_students(data))

@app.route('/assignment/<int:assignment_id>/save_grades', methods=['POST'])
def save_grades(assignment_id):
    student_id_list=request.form.getlist('student_id')
    grade_list=request.form.getlist('grade')
    for student_id, grade in zip(student_id_list, grade_list): 
        data={
            'assignment_id':assignment_id,
            'student_id':int(student_id),
            'grade': float(grade)
        }
        if not Grade.exists_for_student(data):
            Assignment.save_grades(data)
        else:
            Assignment.update_grades(data)

    return redirect('/dashboard')

@app.route('/delete/<int:assignment_id>')
def delete_assignment(assignment_id):
    data={
        'id':assignment_id
    }
    Assignment.delete(data)
    return redirect('/dashboard')

