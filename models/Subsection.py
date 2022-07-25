from extensions.database import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship


class Subsection(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    subsection_name = db.Column(db.String, nullable=False)
    user = relationship("User", back_populates="subsection")
    defibrillator = relationship("Defibrillator", back_populates="subsection")

    serialize_only = ('id', 'subsection_name')

    def __repr__(self):
        return f"{self.subsection_name}"
