from cloudinary import uploader
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import render_template, flash, request, redirect, url_for
from . import student
from website.models.course import Course
from website.models.student import Student
from website.forms.forms import studentForm, EditstudentForm
import re

@student.route('/students')
def view_studs():
    students = Student.get()
    courses = Course.all()

    return render_template("students.html", studentdetails=students, courses = courses)

@student.route('/students/add-student', methods=['GET', 'POST'])
def add_student():
    form = studentForm()
    existing_courses = Course.all()

    course_choices = [(course[0], f"{course[0]} - {course[1]}") for course in existing_courses]
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


@student.route('/view/<string:id>/edit-student', methods=['GET', 'POST'])
def edit_student(id):
    form = EditstudentForm()
    existing_courses = Course.all()
    stud = Student.fetch(id)

    pic = stud[1]

    course_choices = [(course[0], f"{course[0]} - {course[1]}") for course in existing_courses]
    form.course.choices = course_choices

    if form.validate_on_submit():
        if form.pic.data:
            if form.id.data!=id:
                # Checks if the new id input is already used
                checkID = Student.check_id(form.id.data)
                if checkID:
                    flash('ID already exists! Try another one!', category='error')
                    return redirect('/students')
            
            # Upload image to Cloudinary
            upload_result = upload(form.pic.data, folder='SSIS')
            new_pic = upload_result['secure_url']
            student = Student(id=form.id.data, pic=new_pic, fname=form.fname.data, lname=form.lname.data, course=form.course.data, gender=form.gender.data, level=form.level.data)
            student.edit(id)
            public_id = Student.get_public_id_from_url(pic)
            if 'static' not in pic:
                print(public_id)
                result = uploader.destroy(public_id)
            
            flash('Student editted successfully!', category='success')
            if 'result' in result and result['result'] == 'ok':
                print(f"Deleted file {stud[1]} from Cloudinary successfully.")
                    
            else:
                print(f"Failed to delete file {public_id} from Cloudinary. Result: {result}")

            return redirect('/students')
        else:
            if form.id.data!=id:
                # Checks if the new id input is already used
                checkID = Student.check_id(form.id.data)
                if checkID:
                    flash('ID already exists! Try another one!', category='error')
                    return redirect('/students')
            
            student = Student(id=form.id.data, fname=form.fname.data, lname=form.lname.data, course=form.course.data, gender=form.gender.data, level=form.level.data)
            student.edit_without(id)     
                
            flash('Student edited successfully!', category='success')
            return redirect('/students')

    form.id.data = stud[0]
    form.fname.data = stud[2]
    form.lname.data = stud[3]
    form.course.data = stud[4]
    form.gender.data = stud[5]
    form.level.data = stud[6]


    return render_template("edit_student.html", form=form, pic=pic)
    

@student.route('/<string:id>/delete-student', methods=['GET', 'POST'])
def delete_student(id):
    if id:
        student = Student(id=id)
        pic = Student.get_pic(id)
        print(pic)
        public_id = Student.get_public_id_from_url(pic[0])
        print(public_id)
        if 'static' not in pic[0]:
            result = uploader.destroy(public_id)
            if 'result' in result and result['result'] == 'ok':
                print(f"Deleted file {pic} from Cloudinary successfully.")          
            else:
                print(f"Failed to delete file {public_id} from Cloudinary. Result: {result}")
        flash('Student deleted successfully', 'success')
        student.delete()
    else:
        flash('Failed to delete the student', 'error')

    return redirect('/students')

@student.route('/view/<string:id>', methods=['GET'])
def read(id):
    student = Student.view(id)
    #print(student)

    return render_template("/view.html", student=student)