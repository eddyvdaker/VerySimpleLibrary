# app/__init__.py

import logging
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import SMTPHandler, RotatingFileHandler


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()


def create_app(app_settings='app.config.DevelopmentConfig'):
    app = Flask(__name__)

    # Load settings
    if os.environ.get('app_settings'):
        app_settings=os.environ.get('app_settings')
    app.config.from_object(app_settings)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    # Register Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.users import bp as users_bp
    app.register_blueprint(users_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.books import bp as books_bp
    app.register_blueprint(books_bp)

    from app.authors import bp as authors_bp
    app.register_blueprint(authors_bp)

    # Setup logging
    if not app.debug and not app.config['TESTING'] and not app.config['DEV']:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/vsl.log', maxBytes=5120,
                                           backupCount=10)

        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('VSL Startup')

    return app
