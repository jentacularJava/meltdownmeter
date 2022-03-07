# Meltdown Meter
#### Video Demo:  <URL HERE>
#### Description:

Meltdown meter is a tool for people (typically caregivers of children) to track behaviour. The goal is to add an entry every time the behaviour (e.g., a meltdown) occurs, log the details on what triggered the meltdown, what happened during the meltdown, and what made it end. This can help you identify patterns in the behaviour, which can help you reduce the intensity, duration, and/or frequency of the meltdownsn. You can also bring this information to your child's doctor's appointments and the doctor can help analyze the information and make suggestions. At first you could use this to track the baseline of the behaviours. Try to track behaviours for at least one week to get a good sample. Then once you start using any new therapies, track the behaviour again and see if there has been a difference.

There are a number of features and improvements I would like to add in future iterations of this app.

A few ideas include:
- On the "add" page:
- A field for intensity
- A field for duration
- A start/stop timer option for duration
- A contact me page
- Add and edit email addresses to user profile
- Add suggestions box
- Format the date and time in the tables
- Make the fonts and logos nicer looking
- Add photos
- Add child profiles within each user profile so you can add entries for more than one child and keep them separate
- Make usernames case insensitive
- Add sorting and filtering options on the index and entries pages

## Built upon CS50 pset9 Finance
I used a large portion of code from the pset9 Finance since I wanted similar functionalities. This app uses Flask, Jinja, and Bootstrap frameworks. SQLite3 for the database management. requirements.txt is from the original pset files.

## layout.html
This is the template page that has the navbar and footer, which is on every page.

## register.html
This page allows you to register (i.e., add a user into the database).

## login.html
This page allows you to log in. A session is started once you've registered or logged in.

## about.html
This page gives a brief explanation on what Meltdown Meter is.

## add.html
This page allows you to add an entry.

## index.html
This is the landing page of the website, which shows you all previous entries if you are logged in, otherwise it brings you to the login page. The decorator for this route pulls data from the meltdown.db using sqlite3.

## apology.html
This is the apology page, which appears when you run into an error. Error checking happens on all input fields. For example, when you try to sign up but the username is taken or your passwords don't match, when you try to submit empty required fields, or when username/password doesn't match.

## entries.html
This page shows all the previous entries, pulls from meltdown.db.

## account.html
This page shows your account info, and allows you to change your password. After I add more features to this page, I will move the change password function into its own page. But for now, since it's the only action on this page, I decided to keep it simple and allow you to change your password directly from here.

## app.py
This is the main python file that renders all the templates and has all the decorators.

## helpers.py
This file has additional function definitions, such as apology and the login required decorator.

## styles.css
This is the CSS file that is used in addition to Bootstrap.

## meltdown.db
This database contains 3 tables. Users stores all the user's details, such as username, hash, and account creation timestamp. Entries stores all the entries inputted by the user. There are extra columns to use later when I add more features to the entries page. There's a table named children, which is currently empty, but it will be used for when we add the feature to create entries for more than one child per user.