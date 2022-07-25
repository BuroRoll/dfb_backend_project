from sqlalchemy_serializer import SerializerMixin
from extensions.database import db
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from passlib.hash import sha256_crypt
from sqlalchemy import event


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    second_name = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String, nullable=False)
    subsection_id = Column(Integer, ForeignKey("subsection.id"))
    subsection = relationship("Subsection", back_populates="user")
    password = db.Column(db.String, nullable=False)
    log = relationship('Log', back_populates="user")

    excluded_list_columns = ('password',)
    serialize_only = ('id', 'login', 'first_name', 'second_name', 'patronymic', 'subsection')

    def __repr__(self):
        return f"User: {self.login}, {self.first_name}, {self.second_name}"


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, old_value, initiator):
    if value != old_value:
        return sha256_crypt.encrypt(value)
    return value
