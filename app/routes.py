from flask import render_template, flash, redirect, url_for
from app import app
import os

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'DirtSat Admin'}
    return render_template('index.html', title='Home', user=user)
