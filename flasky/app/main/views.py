from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user

from . import main
from .. import db
from .forms import ReminderForm, DeleteReminderForm
from ..models import User, Reminder
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date, timedelta


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/calendar')
def calendar():
    today = date.today()
    year = today.year
    month = today.month
    return render_template('calendar.html', year=year, month=month, today=today)

# handle the AJAX request
@main.route('/calendar-data/<string:date>')
def calendar_data(date):
    year, month, _ = date.split("-")
    month_start = datetime(int(year), int(month), 1)
    month_end = month_start.replace(month=month_start.month % 12 + 1, day=1) - timedelta(days=1)
    days_in_month = month_end.day
    start_day = month_start.weekday()
    calendar = []
    week = [0] * start_day
    for day in range(1, days_in_month+1):
        week.append(day)
        if len(week) == 7:
            calendar.append(week)
            week = []
    if week:
        calendar.append(week + ['-'] * (7-len(week)))
    return jsonify({
        "calendar": calendar,
        "month": month_start.strftime("%m"),
        "year": year,
    })


@main.route('/user/<string:username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    reminders = Reminder.query.filter_by(user_id=user.uid).order_by(Reminder.note_set_date, Reminder.date_start_hour).all()
    most_recent_reminder = None
    for reminder in reminders:
        if datetime.combine(reminder.note_set_date, datetime.min.time()) >= datetime.now():
            most_recent_reminder = reminder
            break
    return render_template('user.html', user=user, most_recent_reminder=most_recent_reminder, len_reminders=len(reminders))


@main.route('/calendar/reminders/<string:date>', methods=['GET', 'POST'])
@login_required
def reminders_on_date(date):
    reminders = Reminder.query.filter_by(user_id=current_user.uid, note_set_date=datetime.strptime(date, '%Y-%m-%d').date()).all()
    form = DeleteReminderForm()
    form.reminder_date.data = date
    
    if form.validate_on_submit():
        reminder = Reminder.query.filter_by(user_id=current_user.uid, note_id=form.reminder_id.data, note_set_date=form.reminder_date.data).first()
        if not reminder:
            flash('Reminder not found.')
            return redirect(url_for('.reminders_on_date', date=date))
        db.session.delete(reminder)
        db.session.commit()
        flash('Reminder deleted.')
        return redirect(url_for('.reminders_on_date', date=date))
    
    return render_template('edit_reminder.html', reminders=reminders, date=date, form=form)


@main.route("/calendar/reminders/process_reminder", methods=["POST", "GET"])
@login_required
def process_reminder():
    form = ReminderForm(request.form)
    if form.validate_on_submit():
        user_id = current_user.uid
        note_name = form.note_name.data
        note_id = form.note_id.data
        note_set_date = form.note_set_date.data
        date_start_hour = form.start_time.data.strftime('%H:%M:%S')
        date_end_hour = form.end_time.data.strftime('%H:%M:%S')
        note_loc = form.note_loc.data
        
        reminder = Reminder(
            note_name=note_name, note_id=note_id, user_id=user_id,
            note_loc=note_loc, note_set_date=note_set_date,
            date_start_hour=date_start_hour, date_end_hour=date_end_hour
            )
        try:
            db.session.add(reminder)
            db.session.commit()
            flash('Reminder created successfully!')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash("note_id already exists!")
            return redirect(url_for('main.process_reminder'))

    return render_template("process_reminder.html", form=form)