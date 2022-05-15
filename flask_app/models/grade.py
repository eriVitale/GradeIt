from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash


class Grade:
    db='teachers_assignments'
    def __init__(self,data):
        self.id=data['id']
        self.grade=data['grade']
        self.assignment_id=data['assignment_id']
        self.student_id=data['student_id']


    @classmethod
    def get_student_grades(cls,data):
        query="SELECT * FROM grades WHERE student_id=%(student_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        grades=[]
        for row in results:
            grades.append(cls(row))
        return grades

    @classmethod
    def exists_for_student(cls,data):
        query="SELECT * FROM grades WHERE student_id=%(student_id)s AND assignment_id=%(assignment_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def get_grade_by_assignment(cls,data):
        query="SELECT * FROM grades WHERE assignment_id=%(assignment_id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        assignment_grades=[]
        for row in results:
            assignment_grades.append(cls(row))
        return assignment_grades