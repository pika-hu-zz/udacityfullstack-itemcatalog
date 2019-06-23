#!/usr/bin/env python3

## Initial config

import sys
import os

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


## Tables
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date = Column(Date)
    timeStart = Column(Time)
    timeEnd = Column(Time)
    numVolunteers = Column(Integer)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'date': str(self.date),
            'start time': str(self.timeStart),
            'end time': str(self.timeEnd),
            'number of volunteers needed': self.numVolunteers,
            'description': self.description,
            'id': self.id,
        }


class Volunteer(Base):
    __tablename__ = 'volunteer'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    attuid = Column(String(6))
    event_id = Column(Integer, ForeignKey('event.id'))
    event = relationship(Event)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'ATTUID': self.attuid,
            'id': self.id,
        }


## End of file config
engine = create_engine('sqlite:///aspirevolunteertracker.db')

Base.metadata.create_all(engine)