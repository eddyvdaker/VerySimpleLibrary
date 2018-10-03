# app/models.py

from datetime import datetime
from flask_login import UserMixin
from hashlib import sha256
from pycountry import countries
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(254), index=True, nullable=False)
    publish_date = db.Column(db.Date(), index=True)
    file = db.Column(db.String(512), nullable=False, unique=True)
    file_type = db.Column(db.String(32), nullable=False, default='unknown',
                          index=True)
    upload_date = db.Column(db.DateTime(), default=datetime.utcnow)
    file_hash = db.Column(db.String(128), unique=True)
    language_code = db.Column(db.String(8), db.ForeignKey('language.code'))
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Book {self.id}: {self.title}>'

    def set_hash(self):
        hash_func = sha256()
        with open(self.file, 'rb') as file:
            while True:
                data = file.read(65536)     # read file in chunks of 64kb
                if not data:
                    break
                hash_func.update(data)
        self.file_hash = hash_func.hexdigest()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, nullable=False)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean(), default=False)
    uploads = db.relationship('Book', backref='uploader', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), index=True, nullable=False)

    def __repr__(self):
        return f'<Author {self.id}: {self.name}>'


class Language(db.Model):
    code = db.Column(db.String(8), primary_key=True)
    books = db.relationship('Book', backref='language', lazy='dynamic')

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
