from flask_admin.form import validators
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship, validates

from saleapp import db
from datetime import datetime
from flask_login import current_user, UserMixin
import enum


class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.Integer, primary_key=True)
    airport_id = db.Column(db.String(64), unique=True)
    airport_name = db.Column(db.String(64), unique=True)


class Transit(db.Model):
    __tablename__ = 'transit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'))
    description = db.Column(db.String(64), nullable = True)

class Flight(db.Model):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True, autoincrement=True)
    departure = Column(String(50), nullable=False)
    arrival = Column(String(50), nullable=False)
    time = Column(Integer, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    priceA1 = Column(Integer, nullable=False)
    priceA2 = Column(Integer, nullable=False)
    seatA1 = Column(Integer, nullable=False)
    seatA2 = Column(Integer, nullable=False)
    reservations = db.relationship('Reservation', backref='reserved_flight' , lazy =  True)
    transits = db.relationship('Transit', backref='transit_airport' , lazy =  True)

    @property
    def empty(self):
        return self.seatA2 + self.seatA1

    def __str__(self):
        return 'Flight ID %r ' % (self.id)


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    confirmed = db.Column(db.Boolean, default=False)


class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    use_role = Column(Enum(UserRole), default=UserRole.USER)
    reservations = db.relationship('Reservation', backref='User' ,lazy = True)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()
