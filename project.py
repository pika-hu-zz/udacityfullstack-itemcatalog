#!/usr/bin/env python3

import datetime

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Event, Volunteer

app = Flask(__name__)

## Connect to Database and create database session
engine = create_engine('sqlite:///aspirevolunteertracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


## Show all events
@app.route('/')
@app.route('/home/')
def showEvents():
    events = session.query(Event).order_by(asc(Event.date))
    return render_template('events.html', events=events)


## Create a new event
@app.route('/event/new/', methods=['GET', 'POST'])
def newEvent():
    if request.method == 'POST':
        newEvent = Event(name = request.form['name'], date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d'), timeStart = datetime.datetime.time(datetime.datetime.strptime(request.form['timeStart'], '%H:%M')), timeEnd = datetime.datetime.time(datetime.datetime.strptime(request.form['timeEnd'], '%H:%M')), numVolunteers = request.form['numVolunteers'], description = request.form['description'])
        session.add(newEvent)
        flash('New Event %s Successfully Created' % newEvent.name)
        session.commit()
        return redirect(url_for('showEvents'))
    else:
        return render_template('newEvent.html')


## Edit an event
@app.route('/event/<int:event_id>/edit/', methods=['GET', 'POST'])
def editEvent(event_id):
    editedEvent = session.query(Event).filter_by(id=event_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedEvent.name = request.form['name']
        if request.form['date']:
            editedEvent.date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')
        if request.form['timeStart']:
            editedEvent.timeStart = datetime.datetime.time(datetime.datetime.strptime(request.form['timeStart'], '%H:%M'))
        if request.form['timeEnd']:
            editedEvent.timeEnd = datetime.datetime.time(datetime.datetime.strptime(request.form['timeEnd'], '%H:%M'))
        if request.form['numVolunteers']:
            editedEvent.numVolunteers = request.form['numVolunteers']
        if request.form['description']:
            editedEvent.description = request.form['description']
        session.add(editedEvent)
        session.commit()
        flash('Event Successfully Edited %s' % editedEvent.name)
        return redirect(url_for('showEvents'))
    else:
        return render_template('editEvent.html', event=editedEvent, event_id=event_id)


## Delete an event
@app.route('/event/<int:event_id>/delete/', methods=['GET', 'POST'])
def deleteEvent(event_id):
    eventToDelete = session.query(Event).filter_by(id=event_id).one()
    if request.method == 'POST':
        session.delete(eventToDelete)
        flash('%s Successfully Deleted' % eventToDelete.name)
        session.commit()
        return redirect(url_for('showEvents', event_id=event_id))
    else:
        return render_template('deleteEvent.html', event=eventToDelete, event_id=event_id)


## Show volunteers for an event
@app.route('/event/<int:event_id>/')
@app.route('/event/<int:event_id>/volunteers/')
def showVolunteers(event_id):
    event = session.query(Event).filter_by(id=event_id).one()
    volunteers = session.query(Volunteer).filter_by(event_id=event_id).all()
    numVolunteered = session.query(Volunteer).filter_by(event_id=event_id).count()
    return render_template('volunteers.html', volunteers=volunteers, event=event, numVolunteered=numVolunteered)


## Create a new volunteer
@app.route('/event/<int:event_id>/volunteers/new/', methods=['GET', 'POST'])
def newVolunteer(event_id):
    event = session.query(Event).filter_by(id=event_id).one()
    if request.method == 'POST':
        newVolunteer = Volunteer(name=request.form['name'], attuid=request.form['attuid'], event_id=event_id)
        session.add(newVolunteer)
        session.commit()
        flash('New Volunteer %s Successfully Created' % (newVolunteer.name))
        return redirect(url_for('showVolunteers', event_id=event_id))
    else:
        return render_template('newVolunteer.html', event_id=event_id)


## Edit a volunteer
@app.route('/event/<int:event_id>/volunteers/<int:volunteer_id>/edit', methods=['GET', 'POST'])
def editVolunteer(event_id, volunteer_id):
    editedVolunteer = session.query(Volunteer).filter_by(id=volunteer_id).one()
    event = session.query(Event).filter_by(id=event_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedVolunteer.name = request.form['name']
        if request.form['attuid']:
            editedVolunteer.attuid = request.form['attuid']
        session.add(editedVolunteer)
        session.commit()
        flash('Volunteer Successfully Edited')
        return redirect(url_for('showVolunteers', event_id=event_id))
    else:
        return render_template('editVolunteer.html', event_id=event_id, volunteer_id=volunteer_id, volunteer=editedVolunteer)


## Delete a volunteer
@app.route('/event/<int:event_id>/volunteers/<int:volunteer_id>/delete', methods=['GET', 'POST'])
def deleteVolunteer(event_id, volunteer_id):
    event = session.query(Event).filter_by(id=event_id).one()
    volunteerToDelete = session.query(Volunteer).filter_by(id=volunteer_id).one()
    if request.method == 'POST':
        session.delete(volunteerToDelete)
        session.commit()
        flash('Volunteer Successfully Deleted')
        return redirect(url_for('showVolunteers', event_id=event_id))
    else:
        return render_template('deleteVolunteer.html', event_id=event_id, volunteer=volunteerToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host = '0.0.0.0', port = 5000)