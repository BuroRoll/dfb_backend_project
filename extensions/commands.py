from .database import db
from models.User import User
from models.Subsection import Subsection
from models.Defibrillator import Defibrillator
from models.Log import Log


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Drop / Clean database - DANGER ACTION"""
    db.drop_all()


models = [Defibrillator, Subsection, User, Log]


def create_model_table():
    """Create table model in the database"""
    for i in models:
        i.__table__.create(db.engine)


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, create_model_table]:
        app.cli.add_command(app.cli.command()(command))
