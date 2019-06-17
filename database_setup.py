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
class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date = Column(Date)
    timeStart = Column(Time)
    timeEnd = Column(Time)
    numVolunteers = Column(Integer)
    description = Column(String(250))


class Volunteer(Base):
    __tablename__ = 'volunteer'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    attuid = Column(String(6))
    event_id = Column(Integer, ForeignKey('event.id'))
    event = relationship(Event)


## End of file config
engine = create_engine('sqlite:///aspirevolunteertracker.db')

Base.metadata.create_all(engine)