#!/usr/bin/env python3

import datetime

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Event, Volunteer, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "aspire-volunteer-tracker-app"

# Connect to Database and create database session
engine = create_engine('sqlite:///aspirevolunteertracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect/', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;'
    output += 'border-radius: 150px;-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


## User Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


## JSON Endpoint
@app.route('/event/<int:event_id>/JSON')
def eventJSON(event_id):
    event = session.query(Event).filter_by(id=event_id).one()
    volunteers = session.query(Volunteer).filter_by(event_id=event_id).all()
    return jsonify(Event=event.serialize, Volunteers=[i.serialize for i in volunteers])


@app.route('/event/<int:event_id>/volunteers/<int:volunteer_id>/JSON')
def volunteerJSON(event_id, volunteer_id):
    volunteer = session.query(Volunteer).filter_by(id=volunteer_id).one()
    return jsonify(Volunteer=volunteer.serialize)


## Show all events
@app.route('/')
@app.route('/home/')
def showEvents():
    events = session.query(Event).order_by(asc(Event.date))
    return render_template('events.html', events=events)


## Create a new event
@app.route('/event/new/', methods=['GET', 'POST'])
def newEvent():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newEvent = Event(
            name = request.form['name'], 
            date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d'), 
            timeStart = datetime.datetime.time(datetime.datetime.strptime(request.form['timeStart'], '%H:%M')), 
            timeEnd = datetime.datetime.time(datetime.datetime.strptime(request.form['timeEnd'], '%H:%M')), 
            numVolunteers = request.form['numVolunteers'], 
            description = request.form['description'], 
            user_id=login_session['user_id'])
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
    owner = getUserInfo(editedEvent.user_id)
    if owner.id != login_session['user_id']:
        flash("You do not have permission to edit this event. Event owner: %s" % owner.name)
        return redirect(url_for('showEvents'))
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
    owner = getUserInfo(eventToDelete.user_id)
    if owner.id != login_session['user_id']:
        flash("You do not have permission to delete this event. Event owner: %s" % owner.name)
        return redirect(url_for('showEvents'))
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
    owner = getUserInfo(event.user_id)
    volunteers = session.query(Volunteer).filter_by(event_id=event_id).all()
    numVolunteered = session.query(Volunteer).filter_by(event_id=event_id).count()
    return render_template('volunteers.html', volunteers=volunteers, event=event, numVolunteered=numVolunteered, owner=owner)


## Create a new volunteer
@app.route('/event/<int:event_id>/volunteers/new/', methods=['GET', 'POST'])
def newVolunteer(event_id):
    event = session.query(Event).filter_by(id=event_id).one()
    owner = getUserInfo(event.user_id)
    if owner.id != login_session['user_id']:
        flash("You do not have permission to edit this event. Event owner: %s" % owner.name)
        return redirect(url_for('showEvents'))
    if request.method == 'POST':
        newVolunteer = Volunteer(
            name=request.form['name'], 
            attuid=request.form['attuid'], 
            event_id=event_id, 
            user_id=login_session['user_id'])
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
    owner = getUserInfo(editedVolunteer.user_id)
    if owner.id != login_session['user_id']:
        flash("You do not have permission to edit this event. Event owner: %s" % owner.name)
        return redirect(url_for('showEvents'))
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
    owner = getUserInfo(volunteerToDelete.user_id)
    if owner.id != login_session['user_id']:
        flash("You do not have permission to edit this event. Event owner: %s" % owner.name)
        return redirect(url_for('showEvents'))
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
    app.run(host = '0.0.0.0', port = 5000, threaded= False)