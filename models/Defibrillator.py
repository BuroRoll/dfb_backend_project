import datetime
import enum

from extensions.database import db

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from sqlalchemy_serializer import SerializerMixin


class StatusesEnum(enum.Enum):
    ready_to_use = 1
    need_service = 2
    service = 3


class ElementsStatusesEnum(enum.Enum):
    ready_to_use = 1
    need_service = 2


class Defibrillator(db.Model, SerializerMixin):
    id = db.Column(db.String, primary_key=True, autoincrement=False, nullable=True)
    defibrillator_name = db.Column(db.String, nullable=False)
    lat_coordinate = db.Column(db.String, nullable=False)
    long_coordinate = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    status = db.Column(Enum(StatusesEnum), nullable=False)
    battery_status = db.Column(Enum(ElementsStatusesEnum), nullable=False)
    electrodes_status = db.Column(Enum(ElementsStatusesEnum), nullable=False)
    last_service_date = db.Column(db.Date, default=datetime.datetime.utcnow, nullable=False)
    log = relationship('Log', back_populates="defibrillator")
    subsection_id = db.Column(Integer, ForeignKey("subsection.id"))
    subsection = relationship("Subsection", back_populates="defibrillator")

    serialize_only = ('id',)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"{self.defibrillator_name}"
