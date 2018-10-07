# app/config.py

import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class BaseConfig:
    """Base configuration"""
    TESTING = False
    DEV = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-long-random-key'
    TMP_FOLDER = os.environ.get('TMP_FOLDER') or os.path.abspath('/tmp')
    FILE_TYPES = os.environ.get('FILE_TYPES') or ['pdf', 'epub', 'mobi']


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEV = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    FILE_FOLDER = os.path.abspath(os.path.join(basedir, './files'))


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app-test.db')
    FILE_FOLDER = os.path.abspath('/tmp')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    FILE_FOLDER = os.environ.get('FILE_FOLDER')
    FILE_FOLDER = os.path.abspath(os.path.join(basedir, './files'))
