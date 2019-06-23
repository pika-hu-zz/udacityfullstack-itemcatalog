#!/usr/bin/env python3

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Volunteer, Event, Base, User

# Connect to Database and create database session
engine = create_engine('sqlite:///aspirevolunteertracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create Dummy User
User1 = User(
    name="Meow Meow",
    email="meow@meow.com",
    picture=('https://www.catster.com/wp-content/uploads/'
             '2018/07/Savannah-cat-lying-down.jpg'),
    id=1)
session.add(User1)
session.commit()


# Create Princeton Arduino Event
event1 = Event(
    name="Princeton HISPA Smart Traffic Light Arduino Workshop",
    date=datetime.date(2019, 6, 7),
    timeStart=datetime.time(11, 30),
    timeEnd=datetime.time(12, 30),
    numVolunteers=6,
    description=("Located off-site at Princeton University,"
                 " requires training in smart traffic light exercise"),
    user=User1)

session.add(event1)
session.commit()

volunteer1 = Volunteer(
    name="Raymond Hu",
    attuid="rh4570",
    event=event1,
    user=User1)

session.add(volunteer1)
session.commit()

volunteer2 = Volunteer(
    name="Christine Liu",
    attuid="cl0285",
    event=event1,
    user=User1)

session.add(volunteer2)
session.commit()

volunteer3 = Volunteer(
    name="Karla Kimble",
    attuid="kk2749",
    event=event1,
    user=User1)

session.add(volunteer3)
session.commit()

volunteer4 = Volunteer(
    name="Philip Cunningham",
    attuid="pc385w",
    event=event1,
    user=User1)

session.add(volunteer4)
session.commit()

volunteer5 = Volunteer(
    name="Jason Swatsworth",
    attuid="js380r",
    event=event1,
    user=User1)

session.add(volunteer5)
session.commit()

volunteer6 = Volunteer(
    name="Pedro Mirabal",
    attuid="pm1926",
    event=event1,
    user=User1)

session.add(volunteer6)
session.commit()


# Create Middletown General Event
event2 = Event(
    name="Colts Neck Girls General Mentorship",
    date=datetime.date(2019, 6, 17),
    timeStart=datetime.time(10),
    timeEnd=datetime.time(12),
    numVolunteers=10,
    description="Located on-site in Middletown, no training requirement",
    user=User1)

session.add(event2)
session.commit()

volunteer1 = Volunteer(
    name="Philip Cunningham",
    attuid="pc385w",
    event=event2,
    user=User1)

session.add(volunteer1)
session.commit()

volunteer2 = Volunteer(
    name="Christine Liu",
    attuid="cl0285",
    event=event2,
    user=User1)

session.add(volunteer2)
session.commit()

volunteer3 = Volunteer(
    name="Anna Genke",
    attuid="ag064d",
    event=event2,
    user=User1)

session.add(volunteer3)
session.commit()

volunteer4 = Volunteer(
    name="Timothy Geraghty",
    attuid="tg784d",
    event=event2,
    user=User1)

session.add(volunteer4)
session.commit()

volunteer5 = Volunteer(
    name="Emily Lu",
    attuid="el973b",
    event=event2,
    user=User1)

session.add(volunteer5)
session.commit()

volunteer6 = Volunteer(
    name="Prahlad Annamraju",
    attuid="pa0160",
    event=event2,
    user=User1)

session.add(volunteer6)
session.commit()

volunteer7 = Volunteer(
    name="Nick Amuso",
    attuid="na181u",
    event=event2,
    user=User1)

session.add(volunteer7)
session.commit()

volunteer8 = Volunteer(
    name="Vineet Sepaha",
    attuid="vs043t",
    event=event2,
    user=User1)

session.add(volunteer8)
session.commit()

volunteer9 = Volunteer(
    name="Theresa Pham",
    attuid="kp6209",
    event=event2,
    user=User1)

session.add(volunteer9)
session.commit()

volunteer10 = Volunteer(
    name="Samantha Kossey",
    attuid="sk7517",
    event=event2,
    user=User1)
session.add(volunteer10)
session.commit()


# Create Middletown Arduino Event
event3 = Event(
    name="Colts Neck Girls Digital Transformation Arduino Workshop",
    date=datetime.date(2019, 6, 17), timeStart=datetime.time(12),
    timeEnd=datetime.time(13), numVolunteers=10,
    description=("Located on-site in Middletown, requires training"
                 " in digital transformation exercise"),
    user=User1)

session.add(event3)
session.commit()

volunteer1 = Volunteer(
    name="Philip Cunningham",
    attuid="pc385w",
    event=event3,
    user=User1)

session.add(volunteer1)
session.commit()

volunteer2 = Volunteer(
    name="Christine Liu",
    attuid="cl0285",
    event=event3,
    user=User1)

session.add(volunteer2)
session.commit()

volunteer3 = Volunteer(
    name="Anna Genke",
    attuid="ag064d",
    event=event3,
    user=User1)

session.add(volunteer3)
session.commit()

volunteer4 = Volunteer(
    name="Timothy Geraghty",
    attuid="tg784d",
    event=event3,
    user=User1)

session.add(volunteer4)
session.commit()

volunteer5 = Volunteer(
    name="Emily Lu",
    attuid="el973b",
    event=event3,
    user=User1)

session.add(volunteer5)
session.commit()

volunteer6 = Volunteer(
    name="Prahlad Annamraju",
    attuid="pa0160",
    event=event3,
    user=User1)

session.add(volunteer6)
session.commit()

volunteer7 = Volunteer(
    name="Nick Amuso",
    attuid="na181u",
    event=event3,
    user=User1)

session.add(volunteer7)
session.commit()

volunteer8 = Volunteer(
    name="Vineet Sepaha",
    attuid="vs043t",
    event=event3,
    user=User1)

session.add(volunteer8)
session.commit()

volunteer9 = Volunteer(
    name="Theresa Pham",
    attuid="kp6209",
    event=event3,
    user=User1)

session.add(volunteer9)
session.commit()

volunteer10 = Volunteer(
    name="Samantha Kossey",
    attuid="sk7517",
    event=event3,
    user=User1)
session.add(volunteer10)
session.commit()
