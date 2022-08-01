from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from models.User import User
from models.Subsection import Subsection
from models.Defibrillator import Defibrillator
from models.Log import Log, OrderView

from blueprints.auth.views import auth
from blueprints.api.public_api.views import public_api
from blueprints.api.private_api.views import api

import config
from extensions import database, commands


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)

    JWTManager(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # setup all our dependencies
    db = database.init_app(app)
    commands.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(public_api, url_prefix='/public_api')
    app.register_blueprint(api, url_prefix='/api')

    # TODO Переделать панель администрирования
    admin = Admin(app, name='Дефибрилляторы', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Subsection, db.session))
    admin.add_view(ModelView(Defibrillator, db.session))
    admin.add_view(OrderView(Log, db.session))
    return app


if __name__ == "__main__":
    create_app().run()
