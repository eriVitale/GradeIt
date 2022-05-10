from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.teacher import Teacher
from flask_app.models.student import Student


@app.route('/<int:id>/students')
def students(id):
    data={
        'id':id
    }
    return render_template('students.html', teacher=Teacher.get_from_id(data),teacher_students=Teacher.get_teachers_students(data),students=Student.get_all())


@app.route('/add_student/<int:teacher_id>/<int:student_id>')
def add_student(teacher_id,student_id):

    data={
        'teacher_id':teacher_id,
        'student_id':student_id
    }
    if Teacher.teacher_has_student(data):
        print("Teacher has student")
        return render_template('students.html', teacher=Teacher.get_from_teacher_id(data),teachers_students=Teacher.get_teachers_students(data),students=Student.get_all())
    Student.add(data)
    return render_template('students.html', teacher=Teacher.get_from_teacher_id(data),teachers_students=Teacher.get_teachers_students(data),students=Student.get_all())


@app.route('/remove_student/<int:teacher_id>/<int:student_id>')
def remove_student(teacher_id,student_id):
    data={
        'teacher_id':teacher_id,
        'student_id':student_id
    }
    Student.remove(data)
    return render_template('students.html', teacher=Teacher.get_from_teacher_id(data),teachers_students=Teacher.get_teachers_students(data),students=Student.get_all())