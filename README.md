# Logs Analysis

> Raymond Hu

## Overview

This is a reporting tool that extracts summaries from a large database containing newspaper articles as awell as the web server log for the newspaper site. The reports generated answer the following questions:

* What are the three most popular articles of all time? (1st query)
* Who are the most popular article authors of all time? (2nd query)
* On which days did more than 1% of requests lead to errors? (3rd query)

## Code Design

* The code interacts with data extracted from the the *newsdata.sql* file (this can be obtained from Udacity)
* Each report uses a single database query to allow for most of the load to be handled by the database, with minimal post-processing by the Ptyhon code
* Views were created in order to easily execute the 3rd query (above) without modifying the original database

## Technologies Used

* Python3
* PostgreSQL
* Vagrant
* VirtualBox
* Git

## Setup

> Assuming you have Python3, Vagrant, and VitualBox already installed

1. Clone this repository
2. Download the *newsdata.sql* from Udacity and move both *newsdata.sql* and *generate-report.py* (from cloned repository) into the vagrant directory within your VM
3. Start up and log into your VM and change to your vagrant directory
4. Run command ```psql -d news -f newsdata.sql``` to load the data from *newsdata.sql* into your local database
5. Run database using ```psql -d news``` and create views (see below)
6. Run command ```python3 generate-report.py``` to generate the report

## Views

View total number of errors per day:
````sql
    CREATE VIEW totalerrors AS
    SELECT cast(time as date) AS day, count(*) AS errors
    FROM log
    WHERE status = '404 NOT FOUND'
    GROUP BY day;
````
View total number of visits per day:
````sql
    CREATE VIEW totalvisits AS
    SELECT cast(time as date) AS day, count(*) AS visits
    FROM log
    GROUP BY day;
````
View error percentage per day:
````sql
    CREATE VIEW errorpercent AS
    SELECT totalerrors.day, totalerrors.errors, totalvisits.visits,
    (cast(totalerrors.errors as double precision))/(cast(totalvisits.visits as double precision)) * 100 AS errorPercent
    FROM totalerrors, totalvisits
    WHERE totalerrors.day = totalvisits.day;
````