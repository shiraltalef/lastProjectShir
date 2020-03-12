"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from lastProjectShir import app
from lastProjectShir.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from lastProjectShir.Models.QueryFormStructure import QueryFormStructure 
from lastProjectShir.Models.QueryFormStructure import LoginFormStructure 
from lastProjectShir.Models.QueryFormStructure import UserRegistrationFormStructure 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact Page',
        year=datetime.now().year,
        message='Shir Altalef'
    )

@app.route('/about')
def about():
    """Renders the home page."""
    return render_template(
        'about.html',
        title='My Project',
        year=datetime.now().year,
    )




@app.route('/Query', methods=['GET', 'POST'])
def Query():

    Name = None
    Country = ''
    capital = ''
    #df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\capitals.csv'))
    #df = df.set_index('Country')

    form = QueryFormStructure(request.form)
     
    if (request.method == 'POST' ):
        name = form.name.data
        Country = name
        if (name in df.index):
            capital = df.loc[name,'Capital']
        else:
            capital = name + ', no such country'
        form.name.data = ''

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\users.csv'))

    raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template('Query.html', 
            form = form, 
            name = capital, 
            Country = Country,
            raw_data_table = raw_data_table,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
        )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/Data')
def Data():
    """Renders the contact page."""
    return render_template(
        'Data.html',
        title='This is My data Page',
        year=datetime.now().year,
        message='My data is about Alcohol consumption by sex'
    )


@app.route('/DataSet')
def DataSet():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\males-vs-females-who-drank-alcohol-in-last-year.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    """Renders the contact page."""
    return render_template(
        'DataSet.html',
        title='This Data is about Alcohol consumption by sex',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='When we look at gender differences we see that in all countries men are more likely to drink than women.'
    )

@app.route('/DataSet2')
def DataSet2():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\share-of-adults-who-drank-alcohol-in-last-year.csv'))
    raw_data_table2 = df.to_html(classes = 'table table-hover')

    """Renders the contact page."""
    return render_template(
        'DataSet2.html',
        title='Share of adults who drink alcohol',
        raw_data_table2 = raw_data_table2,
        year=datetime.now().year,
        message='The share of adults who drink alcohol is highest across Western Europe and Australia. It is highest in France: In 2010, close to 95 percent of adults in France had drunk alcohol in the preceding year.'
    )

@app.route('/DataSet3')
def DataSet3():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\share-who-have-not-drank-alcohol-in-last-year.csv'))
    raw_data_table3 = df.to_html(classes = 'table table-hover')

    """Renders the contact page."""
    return render_template(
        'DataSet3.html',
        title='This Data is about adults who don’t drink alcohol',
        raw_data_table3 = raw_data_table3,
        year=datetime.now().year,
        message='Global trends on alcohol abstinence show a mirror image of drinking prevalence data. This is shown in the charts as the share of adults who have never drunk alcohol.'
    )