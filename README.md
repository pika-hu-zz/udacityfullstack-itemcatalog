# Item Catalog

> Raymond Hu

## Overview

This is a volunteer tracker for the AT&T Aspire program, created to fulfill the item catalog project requirement for the Udacity Full-Stack Developer Nanodegree. This application provides a list of events containing event details and the volunteers signed up for the event. It is supported by a database with REST endpoints that allow users CRUD capability to modify the database. It also protects write functions with AuthN/AuthZ through Google Federation and implements JSON endpoints.

## Code Design

* The ```database_setup.py``` and ```initialevents.py``` files contain code that setup the database and populate it with inital data
* The ```project.py``` file contains code to start the server

## Technologies Used

* Python3
* HTML
* CSS
* Flask
* SQLAlchemy
* SQLLite
* OAuth
* Vagrant
* VirtualBox
* Git

## Setup

> Assuming you have Python3, Vagrant, VitualBox, Flask, SQLAlchemy, SQLLite, and OAuth modules already installed

1. Clone this repository
2. Start up and log into your VM and change to your vagrant directory
3. Run commands ```python3 database_setup.py``` and ```python3 initialevents.py``` to setup and populate database with initial data
4. Run command ```python3 project.py``` to start server

## Routes

* ```/``` or ```/home/``` - Returns homepage with a list of all events ordered by date
* ```/event/new/``` - Allows user to create a new event (once logged in)
* ```/event/<int:event_id>/edit/``` - Allows user to edit an existing event (if user owns the event)
* ```/event/<int:event_id>/delete/``` - Allows user to delete an event (if user owns the event)
* ```/event/<int:event_id>/``` or ```/event/<int:event_id>/volunteers/``` - Returns event page with event details and volunteers signed up for event
* ```/event/<int:event_id>/volunteers/new/``` - Allows user to add a volunteer to the event (if user owns the event)
* ```/event/<int:event_id>/volunteers/<int:volunteer_id>/edit/``` - Allows user to edit an existing volunteer (if user owns the volunteer)
* ```/event/<int:event_id>/volunteers/<int:volunteer_id>/delete/``` - Allows user to delete a volunteer( if user owns the volunteer)
* ```/login/``` - Returns page allowing user to login
* ```/gconnect/``` - Attempts to log user in using Google Federation
* ```/gdisconnect/``` - Attempts to log out user