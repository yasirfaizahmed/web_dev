import os
import datetime
from flask import Flask, render_template, request, url_for, redirect, make_response, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  firstname = db.Column(db.String(100), nullable=False)
  lastname = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(80), unique=True, nullable=False)
  age = db.Column(db.Integer)
  created_at = db.Column(db.DateTime(timezone=True),
                         server_default=func.now())
  bio = db.Column(db.Text)

  def __repr__(self):
    return f'<Student {self.firstname}>'


@app.route("/")
def index():
  # students = Student.query.all()
  return render_template('index.html')
  # return "Home"


@app.route("/students/", methods=["GET"])
def students():
  output = []
  students = Student.query.all()
  for student in students:
    output.append({"firstname": student.firstname,
                   "lastname": student.lastname,
                   "email": student.email,
                   "age": student.age,
                   "created_at": student.created_at,
                   "bio": student.bio
                   })
  return render_template('students.html', all_students=output)


@app.route("/student/<int:student_id>/", methods=["GET"])
def student(student_id):
  student = Student.query.get_or_404(student_id)
  return render_template('student.html', student=student)


@app.route("/edit-student/<int:student_id>", methods=["POST"])
def student_edit(student_id):
  student = Student.query.get_or_404(student_id)
  new_student: dict = request.json
  student.firstname = new_student.get('firstname')
  student.lastname = new_student.get('lastname')
  student.email = new_student.get('email')
  student.age = new_student.get('age')
  student.bio = new_student.get('bio')

  db.session.add(student)
  db.session.commit()

  return f"edited {student} successfully!"


@app.route("/add-student/", methods=["POST"])
def student_add():
  db.create_all()
  student: dict = request.json    # noqa
  new_student = Student(firstname=student.get('firstname'),
                        lastname=student.get('lastname'),
                        email=student.get('email'),
                        age=student.get('age'),
                        bio=student.get('bio'))
  db.session.add(new_student)
  db.session.commit()

  return f"added {new_student} successfully!"


if __name__ == "__main__":
  app.run()
