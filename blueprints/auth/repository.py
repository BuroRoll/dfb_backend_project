from models.User import User
from passlib.hash import sha256_crypt


class PasswordError(Exception):
    """ Ошибка для невалидного пароля"""
    pass


class UserNotFoundError(Exception):
    """ Ошибка для несуществующего пользователя"""
    pass


def login_user(login, password):
    """
        Поиск пользователя в базе данных и сравнение паролей
    """
    user = User.query.filter_by(login=login).first()
    if user is None:
        raise UserNotFoundError
    if sha256_crypt.verify(password, user.password):
        return user
    else:
        raise PasswordError


def get_user_data(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user
