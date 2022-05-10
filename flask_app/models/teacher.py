from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import student
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
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

        self.students=[]
        self.assignments=[]

    @classmethod
    def save(cls,data):
        print(data)
        query="INSERT INTO teachers (first_name, last_name, email, password, prefix, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(prefix)s, NOW(), NOW())"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_from_email(cls,data):
        query="SELECT * FROM teachers WHERE email=%(email)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def get_from_id(cls,data):
        query="SELECT * FROM teachers WHERE id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_from_teacher_id(cls,data):
        query="SELECT * FROM teachers WHERE id=%(teacher_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_from_teacher_id(cls,data):
        query="SELECT * FROM teachers WHERE id=%(teacher_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_teachers_students(cls,data):
        query="SELECT * FROM teachers_students LEFT JOIN students ON students.id=teachers_students.student_id WHERE teacher_id=%(teacher_id)s"
        results=connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def teacher_has_student(cls,data):
        query="SELECT * FROM teachers_students WHERE teachers_students.teacher_id=%(teacher_id)s AND teachers_students.student_id=%(student_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        print(results)
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
