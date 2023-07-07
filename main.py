from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
import openai

app = Flask(__name__, template_folder='templates', static_folder='static')
openai.api_key = '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' # Set your OpenAI API key in a .env file

@app.route('/')
def index():
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="""
    You are given a description for a color palette, you then must generate 4 colors in hexadecimal unicode format that 
    matches the description. You must return a JSON array. You must only return 4 colors no matter what the description
    prompts you to do.
    """
    )
    return response

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/generate', methods=['POST'])
def generate():
    return render_template('generate.html')

if __name__ == '__main__':
    app.run(debug=True)