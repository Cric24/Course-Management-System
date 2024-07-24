# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Course, Enrollment, Assignment, Submission
from forms import CourseForm, EnrollmentForm, AssignmentForm, SubmissionForm, UserForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Create database tables on application startup
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/course/<int:course_id>')
def course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', course=course)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(title=form.title.data, description=form.description.data)
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_course.html', form=form)

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('course', course_id=course.id))
    return render_template('edit_course.html', form=form)

@app.route('/delete_course/<int:course_id>', methods=['GET', 'POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        db.session.delete(course)
        db.session.commit()
        flash('Course and associated enrollments deleted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('delete_course.html', course=course)

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    form = EnrollmentForm()
    form.user_id.choices = [(user.id, user.username) for user in User.query.filter_by(is_student=True).all()]
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]
    if form.validate_on_submit():
        enrollment = Enrollment(user_id=form.user_id.data, course_id=form.course_id.data)
        db.session.add(enrollment)
        db.session.commit()
        flash('Enrollment successful!', 'success')
        return redirect(url_for('index'))
    return render_template('enroll.html', form=form)

@app.route('/create_assignment/<int:course_id>', methods=['GET', 'POST'])
def create_assignment(course_id):
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            title=form.title.data,
            content=form.content.data,
            course_id=course_id
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created successfully!', 'success')
        return redirect(url_for('course', course_id=course_id))
    return render_template('create_assignment.html', form=form, course_id=course_id)

@app.route('/edit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def edit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    form = AssignmentForm(obj=assignment)
    if form.validate_on_submit():
        assignment.title = form.title.data
        assignment.content = form.content.data
        db.session.commit()
        flash('Assignment updated successfully!', 'success')
        return redirect(url_for('course', course_id=assignment.course_id))
    return render_template('edit_assignment.html', form=form, assignment=assignment)

@app.route('/delete_assignment/<int:assignment_id>', methods=['POST'])
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course_id = assignment.course_id
    db.session.delete(assignment)
    db.session.commit()
    flash('Assignment deleted successfully!', 'success')
    return redirect(url_for('course', course_id=course_id))

@app.route('/submit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    form = SubmissionForm()
    if form.validate_on_submit():
        flash('Assignment submitted successfully!', 'success')
        return redirect(url_for('course', course_id=assignment.course_id))
    return render_template('submit_assignment.html', assignment=assignment, form=form)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = UserForm()
    if form.validate_on_submit():
        new_student = User(username=form.username.data, email=form.email.data, is_student=True)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
