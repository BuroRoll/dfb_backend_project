import datetime

from models.User import User
from models.Defibrillator import Defibrillator
from models.Log import Log


def add_defibrillator_db(device_id, defibrillator_name, lat_coordinate, long_coordinate, location, subsection_id):
    defibrillator = Defibrillator(id=device_id,
                                  defibrillator_name=defibrillator_name,
                                  lat_coordinate=lat_coordinate,
                                  long_coordinate=long_coordinate,
                                  location=location,
                                  status='ready_to_use',
                                  battery_status='ready_to_use',
                                  electrodes_status='ready_to_use',
                                  last_service_date=datetime.datetime.utcnow(),
                                  subsection_id=subsection_id)
    try:
        defibrillator.save()
    except Exception:
        return None
    return defibrillator


def get_all_defibrillators_db(status, user_id):
    user = User.query. \
        filter_by(id=user_id). \
        first()
    Defibrillator.serialize_only = (
        'id', 'defibrillator_name', 'lat_coordinate', 'long_coordinate', 'location', 'status')
    defibrillators_list = Defibrillator.query \
        .filter((Defibrillator.status == status) & (Defibrillator.subsection_id == user.subsection_id)) \
        .order_by(Defibrillator.status.desc()) \
        .all()
    return defibrillators_list


def get_current_defibrillator_db(id):
    Defibrillator.serialize_only = (
        'id', 'defibrillator_name', 'lat_coordinate', 'long_coordinate', 'location', 'status', 'battery_status',
        'electrodes_status', 'last_service_date')
    defibrillator = Defibrillator.query. \
        filter_by(id=id). \
        first()
    return defibrillator


def change_device_status(device_id, new_status):
    try:
        defibrillator = Defibrillator.query. \
            filter_by(id=device_id). \
            first()
        defibrillator.status = new_status
        defibrillator.save()
        return defibrillator
    except Exception:
        return None


def get_device_logs_db(device_id):
    Log.serialize_only = ('id', 'user', 'date_log', 'status_code', 'tag')
    logs_list = Log.query \
        .filter_by(defibrillator_id=device_id) \
        .order_by(Log.date_log.desc()) \
        .all()
    return logs_list


def get_device_db(device_id):
    defibrillator = Defibrillator.query. \
        filter_by(id=device_id). \
        first()
    return defibrillator
