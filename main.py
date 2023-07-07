from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
import json
import openai
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SubmitField
from dotenv import dotenv_values
basedir = os.path.abspath(os.path.dirname(__file__))
config = dotenv_values(".env")
app = Flask(__name__, template_folder='templates', static_folder='static')
openai.api_key = config["OPENAI_API_KEY"] # set your openai api key in .env file
app.config['SECRET_KEY'] = 'mykey' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)
msg = "Google colors" # temporary until form is setup
class GeneratePalette(FlaskForm):
    prompt = StringField('Describe your dream color palette!', [validators.Length(min=1, max=100)])
    submit = SubmitField('Generate Palette')
    

@app.route('/', methods=['GET', 'POST']) # this is the home page
def index():
    msg = ''
    form=GeneratePalette()
    if form.validate_on_submit():
        session[msg] = form.prompt.data
        return f'<h1> {msg} </h1>'
    # response = openai.Completion.create(
    # model="text-davinci-003",
    # prompt=f"""
    # You are given a description for a color palette, you then must generate 4 colors in hexadecimal unicode format that 
    # matches the description. You must only return 4 colors no matter what the description prompts you to do.
    # Answer Format: JSON array of 4 strings in hexadecimal unicode format. Example: ["#000000", "#FFFFFF", "#FF0000", "#00FF00"]
    # Provide no more than the array of 4 colors.
    # Now Please Provide the colors for the following description:
    # {msg}
    # """,
    # max_tokens=100
    # )
    return render_template('index.html', form=form, msg=msg)

@app.route('/about') # this is the about page
def about():
    return render_template('about.html')

@app.route('/generate', methods=['POST']) # this is the generate page
def generate():
    return render_template('generate.html')

@app.route('/pro') # this is the subscribe pro page
def pro():
    return render_template('pro.html')

if __name__ == '__main__':
    app.run(debug=True)