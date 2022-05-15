import this
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import student
from flask_app.models import assignment
from flask_app.models import grade
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Teacher:
    db='teachers_assignments'
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.prefix=data['prefix']
        self.account_type=data['account_type']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

        self.students=[]
        self.assignments=[]

    @classmethod
    def save(cls,data):
        print(data)
        query="INSERT INTO teachers (first_name, last_name, email, password, prefix, account_type, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(prefix)s, %(account_type)s, NOW(), NOW())"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_from_email(cls,data):
        query="SELECT * FROM teachers WHERE email=%(email)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        else:
            return cls(results[0])

    @classmethod
    def get_students_teachers(cls,data):
        query="SELECT * FROM teachers_students WHERE student_id=%(student_id)s; "
        results=connectToMySQL(cls.db).query_db(query,data)
        this_students_teachers=[]
        for row in results:
            teacher={
                'teacher_id':row['teacher_id']
            }
            this_students_teachers.append(teacher)

        return this_students_teachers


    @classmethod
    def get_from_id(cls,data):
        query="SELECT * FROM teachers WHERE id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_from_teacher_id(cls,data):
        query="SELECT * FROM teachers WHERE id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_teachers_students(cls,data):
        query="SELECT * FROM teachers LEFT JOIN teachers_students ON teachers_students.teacher_id=teachers.id LEFT JOIN students ON students.id=teachers_students.student_id WHERE teachers.id=%(id)s"
        results=connectToMySQL(cls.db).query_db(query,data)
        this_teacher=cls(results[0])
        for row in results:
            student_data={
                "id":row['students.id'],
                "first_name":row['students.first_name'],
                "last_name":row['students.last_name'],
                "email":row['students.email'],
                "password":row['students.password'],
                'prefix':row['students.prefix'],
                "account_type":row['students.account_type'],
                "created_at":row['students.created_at'],
                "updated_at":row['students.updated_at'],
            }
            one_student=student.Student(student_data)
            one_student.grades=grade.Grade.get_student_grades({'student_id':row['students.id']})
            this_teacher.students.append(one_student)
            print (this_teacher.students)
        return this_teacher

    @classmethod
    def teacher_has_student(cls,data):
        query="SELECT * FROM teachers_students WHERE teachers_students.teacher_id=%(id)s AND teachers_students.student_id=%(student_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return results

    @staticmethod
    def validate_user(teacher):
        is_valid=True
        query="SELECT * FROM teachers WHERE email=%(email)s;"
        results=connectToMySQL(Teacher.db).query_db(query,teacher)
        if results:
            flash("Email already taken.")
            is_valid=False
        if not EMAIL_REGEX.match(teacher['email']):
            flash("Invalid email address")
            is_valid=False
        if len(teacher['first_name'])<2 or teacher['first_name'].isalpha()==False:
            flash("*First name must be at least 2 characters and consist of only alphabetic characters")
            is_valid=False
        if len(teacher['last_name'])<2 or teacher['last_name'].isalpha()==False:
            flash("*Last name must be at least 2 characters and consist of only alphabetic characters")
            is_valid=False
        if len(teacher['password']) <8:
            flash("*Password must be at least 8 characters")
            is_valid=False
        if teacher['confirm_password'] != teacher['password']:
            flash("*Confirm Password must match Password field")
            is_valid=False
        if teacher['prefix']=='Prefix':
            flash("*Please select a preferred prefix.")
        return is_valid
