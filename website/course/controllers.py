from flask import render_template, flash, request, redirect
from . import course
from website.models.course import Course
from website.models.college import College

@course.route('/courses')
def curs():
    courses = Course.all()
    print(courses)
    colleges = College.all()
    print(colleges)

    return render_template("courses.html", coursedetails=courses, colleges = colleges)

@course.route('/add-course', methods=['GET', 'POST'])
def add_course():
    colleges = College.all()
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        college = request.form.get('college')

        col = Course.check_college(college)
        check_code = Course.check_code(code)

        if check_code:
            flash('This course already exists!', category='error')
        else:
            if col:
                if len(code) < 1:
                    flash('This cannot be empty!', category='error')
                if len(name) < 1:
                    flash('This cannot be empty!', category='error')
                elif len(college) < 1:
                    flash('An associated college must exist!', category='error')
                else:
                    #add course to database
                    course = Course(code=code, name=name, college=college)
                    course.add()
                    flash('Course added successfully!', category='success')
                    return redirect('/courses')
            else:
                flash('College does not exist!', category='error')

    return render_template("add_course.html", colleges = colleges)

@course.route('/edit-course', methods=['GET', 'POST'])
def edit_course():
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        college = request.form.get('college')
        newcode = request.form.get('newcode')

        # Check if the college exists in the colleges table
        existing_college = Course.check_college(college)

        if newcode == code:
            if existing_college:
                # The college exists, so you can proceed with the UPDATE query
                course = Course(code=code, name=name, college=college)
                course.edit()
                flash('Course editted successfully!', category='success')
            else:
                # The college code doesn't exist in the colleges table
                flash('College does not exist!', category='error')
        else:
            check = Course.check_code(newcode)
            if check:
                flash('Course code already in use! Try another one.', category='error')
            else:
                if existing_college:
                    # The college exists, so you can proceed with the UPDATE query
                    course = Course(code=code, name=name, college=college)
                    course.edit()
                    course.editcode(newcode)
                    flash('Course editted successfully!', category='success')
                else:
                    # The college code doesn't exist in the colleges table
                    flash('College does not exist!', category='error')
    
    return redirect('/courses')

@course.route('/delete-course', methods=['POST'])
def delete_course():
    code = request.form.get('course_code')

    if code:
        course = Course(code=code)
        course.delete()
        flash('Course deleted successfully', 'success')
    else:
        flash('Failed to delete the Course', 'error')

    return redirect('/courses')