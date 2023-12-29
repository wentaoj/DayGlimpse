from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Regexp

class ReminderForm(FlaskForm):
    note_name = StringField("Reminder Name", default="New Reminder", validators=[DataRequired()])
    note_id = StringField('Reminder ID', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z0-9_]*$', message='Reminder ID must only contain letters, numbers or underscores')]) # PK: note_id
    note_set_date = DateField('Reminder Date Selection: ', 
                              format='%Y-%m-%d', 
                              validators=[DataRequired()], 
                              default=date.today() + timedelta(days=1)
                              )
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    note_loc = StringField("Location (optional)", default="online meeting room")
    addition = TextAreaField("Additional Information")
    submit = SubmitField("Submit")

class DeleteReminderForm(FlaskForm):
    reminder_id = StringField('Reminder ID', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z0-9_]*$', message='Reminder ID must only contain letters, numbers or underscores')])
    reminder_date = StringField('Reminder Date', validators=[DataRequired()])
    submit = SubmitField('Delete Reminder')
