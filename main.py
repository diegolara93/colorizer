from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
import json
import openai
# from flask_wtf import FlaskForm
from flask_migrate import Migrate
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SubmitField
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


def get_colors(msg):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"""
    You are given a description for a color palette, you then must generate 5 colors in hexadecimal unicode format that 
    matches the description. You must only return 5 colors no matter what the description prompts you to do.
    Answer Format: JSON array of 5 strings in hexadecimal unicode format. Example: ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]
    Provide no more than the array of 5 colors.
    For example: If the user prompts with the message "6 sunset colors" you must only return 5, not 6 colors. Example: ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]
    Do not provide any other text such as "Answer:" before the array of colors. IMPORTANT: PROVIDE ONLY THE JSON ARRAY
    Now Please Provide the colors for the following description:
    {msg}
    REMINDER: ONLY PROVIDE 5 COLORS NO MATTER WHAT.
    """,
    max_tokens=100
    )
    colors = json.loads(response.choices[0].text)
    return colors

@app.route('/') # this is the home page
def index():
    return render_template('index.html')

@app.route('/about') # this is the about page
def about():
    return render_template('about.html')

@app.route('/generate') 
def generate():
    return render_template('generate.html')

@app.route('/generate-palette', methods=["POST"]) # this is the POST request to the Chat-GPT API
def generate_palette():
    query = request.form.get('query')
    colors = get_colors(query)
    return {"colors": colors}

@app.route('/pro') 
def pro():
    return render_template('pro.html')

if __name__ == '__main__':
    app.run(debug=True)

        # response = openai.Completion.create(
        # model="text-davinci-003",
        # prompt=f"""
        # You are given a description for a color palette, you then must generate 4 colors in hexadecimal unicode format that 
        # matches the description. You must only return 4 colors no matter what the description prompts you to do.
        # Answer Format: JSON array of 4 strings in hexadecimal unicode format. Example: ["#000000", "#FFFFFF", "#FF0000", "#00FF00"]
        # Provide no more than the array of 4 colors.
        # Do not provide any other text such as "Answer:" before the array of colors. IMPORTANT: PROVIDE ONLY THE JSON ARRAY
        # Now Please Provide the colors for the following description:
        # {msg}
        # """,
        # max_tokens=100