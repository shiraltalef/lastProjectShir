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

import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from lastProjectShir.Models.QueryFormStructure import QueryFormStructure 
from lastProjectShir.Models.QueryFormStructure import LoginFormStructure 
from lastProjectShir.Models.QueryFormStructure import UserRegistrationFormStructure 
from lastProjectShir.Models.QueryFormStructure import AlcoholFrom 

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


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




@app.route('/query' , methods = ['GET' , 'POST'])
def query():

    print("query")

    form1 = AlcoholFrom()
    chart = "https://cdn.psychologytoday.com/sites/default/files/styles/article-inline-half/public/field_blog_entry_images/shutterstock_289559648.jpg?itok=PytdvWHB" 

   # reading the csv file
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/males-vs-females-who-drank-alcohol-in-last-year.csv'))
    #chancing the name of the columns to make life simpler
    df = df.rename(columns={"Share of females who have drank alcohol in last year (%)":"Females", "Share of males who have drank alcohol in last year (%)":"Males", "Entity":"Country"})
    #sating index to country
    df=df.set_index("Country")
    #removing nans
    df=df[df["Females"].notna()]
    df=df[df["Males"].notna()]
    #prepring choices for form
    l=df.index.tolist()
    form1.countries.choices=list(zip(l,l))
    df=df[['Males','Females']]

    
       #this is where submit happens
    if request.method == 'POST':
        countries= form1.countries.data
        df=df.loc[countries]

     
        fig = plt.figure()
        fig.subplots_adjust(bottom=0.4)
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'bar', figsize = (24, 8) , fontsize = 22 , grid = True)
        chart = plot_to_img(fig)

    
    return render_template(
        'query.html',
        form1 = form1,
        chart = chart
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
            return redirect('/query')
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

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String