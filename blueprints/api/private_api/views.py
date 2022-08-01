import json

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from models.Log import StatusCodeEnum, tags
from .repository import *
from ...auth.repository import get_user_data

api = Blueprint('api', __name__)


@api.route('/add_defibrillator', methods=['POST'])
@jwt_required()
def add_defibrillator():
    """ Добавление нового дефибриллятора """
    user_id = get_jwt_identity()
    device_id = request.json.get('device_id', None)
    defibrillator_name = request.json.get('defibrillator_name', None)
    location = request.json.get('location', None)
    lat_coordinate = request.json.get('lat_coordinate', None)
    long_coordinate = request.json.get('long_coordinate', None)
    user = get_user_data(user_id)
    defibrillator = add_defibrillator_db(device_id,
                                         defibrillator_name,
                                         lat_coordinate,
                                         long_coordinate,
                                         location,
                                         user.subsection_id)
    Log(user_id=user_id, defibrillator_id=defibrillator.id, status_code=StatusCodeEnum.information, tag=tags['Create'])
    if defibrillator is None:
        return jsonify(error='Не удалось сохранить дефибриллятор')
    return jsonify(id=defibrillator.id, status='1', coordinates=(lat_coordinate, long_coordinate))


@api.route('/defibrillator_list/<status>', methods=['GET'])
@jwt_required()
def get_all_defibrillators(status):
    """ Получение всех дефибрилляторов с определённым статусом """
    claims = get_jwt()
    user_id = claims['user_id']
    defibrillators_list = get_all_defibrillators_db(status, user_id)
    return json.dumps([r.to_dict() for r in defibrillators_list])


@api.route('/get_defibrillator/<id>', methods=['GET'])
@jwt_required()
def get_current_defibrillator(id):
    """ Получение данных о конкретном дефибрилляторе """
    defibrillator = get_current_defibrillator_db(id)
    return json.dumps(defibrillator.to_dict())


@api.route('/service_device/<device_id>', methods=['PUT'])
@jwt_required()
def service_device(device_id):
    device = get_device_db(device_id)
    old_status = device.status.name
    new_status = ''
    if device.status.name == 'need_service' or device.status.name == 'ready_to_use':
        device.status = 'service'
        new_status = 'service'
    else:
        device.status = 'ready_to_use'
        new_status = 'ready_to_use'
    device.save()
    return jsonify(old_status=old_status, new_status=new_status)


@api.route('/logs/<device_id>', methods=['GET'])
@jwt_required()
def get_device_logs(device_id):
    """ Получение логов для конкретного устройства """
    device_logs = get_device_logs_db(device_id)
    if device_logs is None:
        return jsonify(error='Не удалось получить данные, попробуйте позже')
    return json.dumps([r.to_dict() for r in device_logs])


@api.route('/check_device/<device_id>', methods=['GET'])
@jwt_required()
def check_device(device_id):
    """ Проверка наличия устройства в базе данных """
    device = get_device_db(device_id)
    if device is None:
        return jsonify(error='no device in database'), 204
    else:
        return jsonify(device_id=device_id), 200
