# app/models.py

from pycountry import countries
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

    @staticmethod
    def to_name(code):
        try:
            if len(code) == 2:
                return countries.get(alpha_2=code).name
            elif len(code) == 3:
                return countries.get(alpha_3=code).name
            else:
                return 'invalid country code'
        except KeyError:
            return 'country code does not match a known country'

    @staticmethod
    def to_code(country, code_len=2):
        try:
            if code_len == 3:
                return countries.get(name=country).alpha_3
            else:
                return countries.get(name=country).alpha_2
        except KeyError:
            return 'country not found'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
