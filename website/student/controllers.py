from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import render_template, flash, request, redirect, url_for
from . import student
from website.models.course import Course
from website.models.student import Student
from website.forms.forms import studentForm
import re

@student.route('/students')
def view_studs():
    #students = models.Student.all()
    students = Student.get()
    courses = Course.all()
    

    return render_template("students.html", studentdetails=students, courses = courses)

@student.route('/students/add-student', methods=['GET', 'POST'])
def add_student():
    form = studentForm()
    existing_courses = Course.all()

    course_choices = [(course.code, f"{course.code} - {course.name}") for course in existing_courses]
    form.course.choices = course_choices

    if form.validate_on_submit():
        exists = Student.check_id(form.id.data)
        course_code = form.course.data

        # Check if the selected course exists
        if not Course.check_code(course_code):
            flash('Invalid course selected!', category='error')
            return render_template("add_student.html", form=form)

        if exists:
            flash('This ID already exists!', category='error')
        else:
            if form.pic.data:
                # Upload image to Cloudinary
                upload_result = upload(form.pic.data, folder='SSIS')
                pic = upload_result['secure_url']
            else:
                # Set a default profile picture URL or handle it as per your requirements
                pic = url_for('static', filename='img/default_profilepic.png')

            # Add student to the database
            student = Student(id=form.id.data, pic=pic, fname=form.fname.data, lname=form.lname.data, course=course_code, gender=form.gender.data, level=form.level.data)
            student.add()
            flash('Student added successfully!', category='success')
            return redirect('/students')

    return render_template("add_student.html", form=form)


@student.route('/edit-student', methods=['GET', 'POST'])
def edit_student():
    if request.method == 'POST':
        studID = request.form.get('id')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        course = request.form.get('course')
        gender = request.form.get('gender')
        level = request.form.get('level')
        newID = request.form.get('newID')

        if not studID or not fname or not lname or not gender or not course or not level:
            flash('Please fill out all fields!', category='error')
            return redirect('/students')

        # Check if the new ID follows the right format
        if not re.match(r'^\d{4}-\d{4}$', newID):
            flash('New ID should follow the format YYYY-NNNN', category='error')
            return redirect('/students')
        
        # Check if the gender is valid
        if gender not in ['Male', 'Female']:
            flash('Gender should be "Male" or "Female"', category='error')
            return redirect('/students')
        
        # Check if the course code exists in the courses table
        existing_course = Student.check_course(course)

        # Check if the ID is updated
        if newID == studID:
            if existing_course:
                # The course code exists, so you can proceed with the UPDATE query
                student = Student(id=studID, fname=fname, lname=lname, course=course, gender=gender, level=level)
                student.edit()
                
                flash('Student edited successfully!', category='success')
            else:
                    # The course code doesn't exist in the courses table
                    flash('Course does not exist!', category='error')
        else:
            # Checks if the new id input is already used
            checkID = Student.check_id(newID)
            if checkID:
                flash('ID already exists! Try another one!', category='error')
            else:
                if existing_course:
                    # The course code exists, so you can proceed with the UPDATE query
                    student = models.Student(id=studID, fname=fname, lname=lname, course=course, gender=gender, level=level)
                    # Normal edit first
                    student.edit()
                    # Then change the ID
                    student.editID(newID)
                    
                    flash('Student edited successfully!', category='success')
                else:
                    # The course code doesn't exist in the courses table
                    flash('Course does not exist!', category='error')
    return redirect('/students')

@student.route('/delete-student', methods=['POST'])
def delete_student():
    student_id = request.form.get('student_id')

    if student_id:
        student = Student(id=student_id)
        student.delete()
        flash('Student deleted successfully', 'success')
    else:
        flash('Failed to delete the student', 'error')

    return redirect('/students')

@student.route('/view/<string:id>', methods=['GET'])
def read(id):
    student = Student.fetch(id)
    print(student)

    return render_template("/view.html", student=student)