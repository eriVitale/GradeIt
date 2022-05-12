from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Student:
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

        self.teachers=[]
        self.assignments=[]

    @classmethod
    def save(cls,data):
        print(data)
        query="INSERT INTO students (first_name, last_name, email, password, prefix, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(prefix)s, NOW(), NOW())"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def add(cls,data):
        query="INSERT INTO teachers_students (teacher_id, student_id) VALUES (%(id)s,%(student_id)s); "
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def remove(cls,data):
        query="DELETE FROM teachers_students WHERE student_id=%(student_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query="SELECT * FROM students"
        return connectToMySQL(cls.db).query_db(query)