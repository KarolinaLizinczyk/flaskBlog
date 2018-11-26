from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from celery_config import make_celery

from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)
celery = make_celery(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


mail = Mail(app)
CSRFProtect(app)

from app import models, forms, views

