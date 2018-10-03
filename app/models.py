# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, nullable=False)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Language(db.Model):
    code = db.Column(db.String(8), primary_key=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
