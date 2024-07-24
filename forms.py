from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from models import User, Course

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Student')

class EnrollmentForm(FlaskForm):
    user_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enroll')

    def populate_choices(self):
        self.user_id.choices = [(user.id, user.username) for user in User.query.all()]
        self.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

class CourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Update Course')


class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])  # Update field name
   
    submit = SubmitField('Create Assignment')



class SubmissionForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit Assignment')


