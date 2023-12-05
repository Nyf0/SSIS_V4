from flask import Blueprint, render_template, request
from website.models.student import Student
from website.models.course import Course
from website.models.college import College

views = Blueprint('views', __name__)

@views.route('/')
def home():
    student = Student()
    course = Course()
    college = College()

    #Retrieve last 5 items from each table
    students = student.show()
    courses = course.show()
    colleges = college.show()

    return render_template("home.html", students=students, courses=courses, colleges=colleges)

@views.route('/search', methods=['GET', 'POST'])
def search():
    search_term = request.form['search_term']

    students = Student.search(search_term)
    courses= Course.search(search_term)
    colleges = College.search(search_term)

    return render_template('search.html', students=students, courses=courses, colleges=colleges)

