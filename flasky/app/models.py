from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # need install!
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager


class Reminder(UserMixin, db.Model):
    __tablename__ = "reminder"
    note_name = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    note_id = db.Column(db.Integer, unique=True, primary_key=True) # PK: note_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid')) # FK
    note_loc = db.Column(db.String(64))
    note_set_date = db.Column(db.Date, nullable=False, index=True)
    date_start_hour = db.Column(db.String(64)) 
    date_end_hour = db.Column(db.String(64)) 
    user = db.relationship("User", back_populates="reminder") # 1 to 1

    def __repr__(self):
        return "<note %r>" % self.note_id
    
    def get_id(self):
        return str(self.note_id)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, unique=True, primary_key = True) # PK: uid
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    dob = db.Column(db.Date, default=date.today())
    password_hash = db.Column(db.String(128))
    reminder = db.relationship("Reminder", back_populates="user") # 1 to 1
    
    def __repr__(self):
        return "<user %r>" % self.uid
    
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.uid)  # convert to string as required by Flask-Login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
