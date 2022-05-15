from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.teacher import Teacher
from flask_app.models.student import Student


@app.route('/<int:id>/students')
def students(id):
    data={
        'id':id
    }
    return render_template('students.html', teacher=Teacher.get_teachers_students(data), students=Student.get_all())

@app.route('/student_dashboard')
def studenthome():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'student_id':session['user_id']
    }
    return render_template('student_dashboard.html', student=Student.get_from_id(data))


@app.route('/add_student/<int:student_id>')
def add_student(student_id):
    data={
        'id':session['user_id'],
        'student_id':student_id
    }
    if Teacher.teacher_has_student(data):
        print("Teacher has student")
        return render_template('students.html', teacher=Teacher.get_teachers_students(data),students=Student.get_all())
    Student.add(data)
    return render_template('students.html', teacher=Teacher.get_teachers_students(data), students=Student.get_all())


@app.route('/remove_student/<int:student_id>')
def remove_student(student_id):
    data={
        'id':session['user_id'],
        'student_id':student_id
    }
    Student.remove(data)
    return render_template('students.html',teacher=Teacher.get_teachers_students(data),students=Student.get_all())