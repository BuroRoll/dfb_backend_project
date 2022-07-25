from models.Defibrillator import Defibrillator


def get_available_defibrillators_db():
    Defibrillator.serialize_only = (
        'id', 'defibrillator_name', 'lat_coordinate', 'long_coordinate', 'location', 'status')
    defibrillators_list = Defibrillator.query \
        .filter_by(status='ready_to_use') \
        .all()
    return defibrillators_list


def get_current_defibrillator_db(id):
    Defibrillator.serialize_only = (
        'id', 'defibrillator_name', 'lat_coordinate', 'long_coordinate', 'location', 'status')
    defibrillator = Defibrillator.query. \
        filter_by(id=id). \
        first()
    return defibrillator
