from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app.models import teacher
bcrypt=Bcrypt(app)
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Assignment:
    db='teachers_assignments'
    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.description=data['description']
        self.points=data['points']
        self.date=data['date']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.teacher_id=data['teacher_id']

    @classmethod
    def save_assignment(cls,data):
        query="INSERT INTO assignments (name, description, points, date, created_at, teacher_id) VALUES (%(name)s, %(description)s, %(points)s, %(date)s, NOW(), %(teacher_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)
   
    @classmethod
    def get_teacher_assignments(cls,data):
        query="SELECT * FROM assignments LEFT JOIN teachers ON teachers.id=assignments.teacher_id WHERE teacher_id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        assignments=[]
        for assignment in results:
            assignments.append(cls(assignment))
        for assignment in assignments:
            if assignment.name==None:
                assignments.remove(assignment)
        return assignments

    @classmethod
    def get_from_id(cls,data):
        query="SELECT * FROM assignments WHERE id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def save_grades(cls,data):
        query='UPDATE student_assignments SET student_id=%(student_id)s, assignment_id=%(assignment_id)s, grade=%(grade)s WHERE assignment_id=%(assignment_id)s'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_student_assignments(cls,data):
        query="SELECT * FROM student_assignments WHERE student_id=%(student_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_assignment(assignment):
        is_valid=True
        if len(assignment['name'])<3:
            flash("Assignment name must be at least 3 characters.")
            is_valid=False
        if len(assignment['description'])<5:
            flash("Assignment description must be at least 5 characters")
            is_valid=False
        if not assignment['points'].isnumeric():
            flash("Points value must be numeric")
            is_valid=False
        if int(assignment['points'])<=0:
            flash("Point value must be greater than 0")
            is_valid=False
        if not assignment['date']:
            flash("Please select assignment date")
            is_valid=False
        return is_valid

