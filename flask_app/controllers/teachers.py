
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.teacher import Teacher
from flask_app.models.assignment import Assignment
from flask_app.models.student import Student
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    if not Teacher.validate_user(request.form):
        return redirect('/')
    pw_hash=bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    if request.form['account_type']=='teacher':
        data={
            "first_name": request.form['first_name'],
            "last_name":request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash,
            "prefix":request.form['prefix'],
            'account_type':request.form['account_type'],
        }
        id=Teacher.save(data)
        session['user_id']=id
        return redirect('/dashboard')
    elif request.form['account_type']=='student':
        data={
            "first_name": request.form['first_name'],
            "last_name":request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash,
            "prefix":request.form['prefix'],
            'account_type':request.form['account_type']
        }
        id=Student.save(data)
        session['user_id']=id
        return redirect('/student_dashboard')

@app.route('/login', methods=['POST'])
def login():
    data={'email': request.form['email']}
    user_in_teacher_db=Teacher.get_from_email(data)
    user_in_student_db=Student.get_from_email(data)
    if user_in_teacher_db:
        user_in_db=user_in_teacher_db
    elif user_in_student_db:
        user_in_db=user_in_student_db
    else:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id']=user_in_db.id
    if user_in_teacher_db:
        return redirect('/dashboard')
    else:
        return redirect('/student_dashboard')


    

@app.route('/dashboard')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id': session['user_id'],
        'teacher_id': session['user_id'],
    }
    return render_template('dashboard.html', assignments=Assignment.get_teacher_assignments(data),teacher=Teacher.get_teachers_students(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
