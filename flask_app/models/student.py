from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import assignment
from flask_app.models.assignment import Assignment
from flask_app.models import teacher
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
        
        self.teachers=teacher.Teacher.get_students_teachers({'student_id':data['id']})
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
    def get_from_email(cls,data):
        query='SELECT * FROM students WHERE email=%(email)s;'
        results=connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        else:
            return cls(results[0])

    

    @classmethod
    def get_from_id(cls,data):
        query="SELECT * FROM students LEFT JOIN grades ON grades.student_id=students.id LEFT JOIN assignments on assignments.id=grades.assignment_id WHERE students.id=%(student_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        this_student=cls(results[0])
        for row in results:
            assignment={
                'name':row['name'],
                'points':row['points'],
                'date':row['date'],
                'grade':row['grade']
            }
            this_student.assignments.append(assignment)
        return this_student

    @classmethod
    def remove(cls,data):
        query="DELETE FROM teachers_students WHERE student_id=%(student_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query="SELECT * FROM students"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def update_grades(cls, data):
        query="SELECT * FROM students LEFT JOIN student_assignments ON student_assignments.student_id=students.id LEFT JOIN assignments ON assignments.id=student_assignments.assignment_id WHERE assignments.id=%(assignment_id)s AND students.id=%(student_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        this_student=cls(results[0])
        for row in results:
            assignment_data={ 
                'id':row['assignments.id'],
                'name':row['name'],
                'description':row['description'],
                'points':row['points'],
                'date':row['date'],
                'teacher_id':row['teacher_id'],
                'created_at':row['assignments.created_at'],
                'updated_at':row['assignments.updated_at'],
                'grade':row['grade'],
            }
            this_student.assignments.append(assignment.Assignment(assignment_data))
        return this_student
    
  
