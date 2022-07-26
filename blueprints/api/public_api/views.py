import json

from flask import Blueprint, jsonify

from .repository import *

public_api = Blueprint('public-api', __name__)


@public_api.route('/get_available_defibrillators', methods=['GET'])
def get_available_defibrillators():
    """ Получение списка всех доступных дефибрилляторов """
    defibrillators_list = get_available_defibrillators_db()
    return json.dumps([r.to_dict() for r in defibrillators_list])


@public_api.route('/get_defibrillator/<id>', methods=['GET'])
def get_current_defibrillator(id):
    """ Получение данных по конкретному деффибриллятору """
    defibrillator = get_current_defibrillator_db(id)
    return json.dumps(defibrillator.to_dict())

@public_api.route('/hello', methods=['GET'])
def hello():
    return jsonify(hello='world')
