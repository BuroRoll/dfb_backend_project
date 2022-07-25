import datetime

from flask_admin.contrib.sqla import ModelView
from sqlalchemy_serializer import SerializerMixin


from extensions.database import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import enum
from sqlalchemy import Enum


class StatusCodeEnum(enum.Enum):
    information = 1  # Использовали, создали
    service = 2  # Сняли для обслуживания, заменили батарею, заменили электроды, вернули после обслуживания
    warning = 3  # Критический уровень заряда аккуиулятора, износ электродов


tags = {
    'Create': 'Дефибриллятор добавлен в список',
    'Use': 'Дефибриллятор был использован',
    'Start_service': 'Начало обслуживания',
    'Battery_change': 'Батарея заменена',
    'Electrodes_change': 'Электроды заменены',
    'End_service': 'Обслуживание завершено',
    'Battery_WARNING': 'Критический уровень заряда аккумулятора',
    'Electrodes_WARNING': 'Высокий уровень износа электродов'
}


class Log(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="log")
    defibrillator_id = db.Column(String, ForeignKey("defibrillator.id"))
    defibrillator = relationship("Defibrillator", back_populates="log")
    date_log = db.Column(db.Date, default=datetime.datetime.utcnow, nullable=False)
    status_code = db.Column(Enum(StatusCodeEnum), nullable=False)
    tag = db.Column(db.Text, nullable=False)

    serialize_only = ('id',)

    def __repr__(self):
        return f"{self.status_code} | {self.tag} | {self.date_log}"

    def __init__(self, user_id, defibrillator_id, status_code, tag):
        self.user_id = user_id
        self.defibrillator_id = defibrillator_id
        self.status_code = status_code
        self.tag = tag
        db.session.add(self)
        db.session.commit()


class OrderView(ModelView):
    column_filters = ('user', 'user.id', 'defibrillator', 'defibrillator.id')
