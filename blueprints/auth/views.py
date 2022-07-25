from flask import Blueprint, request, jsonify
from datetime import timedelta
from .repository import *
from flask_jwt_extended import create_access_token, create_refresh_token

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["POST"])
def login():
    """ Авторизация пользователя """
    user_login = request.json.get('login', None)
    password = request.json.get('password', None)
    try:
        user = login_user(user_login, password)
    except UserNotFoundError:
        return jsonify(error='Пользователя с таким логином не найден'), 400
    except PasswordError:
        return jsonify(error='Неверный пароль'), 400
    additional_claims = {"user_id": user.id, }
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1),
                                       additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=300))
    return jsonify(token=access_token,
                   refresh_token=refresh_token,
                   id=user.id,
                   login=user.login,
                   first_name=user.first_name,
                   second_name=user.second_name)
