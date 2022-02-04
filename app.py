from crypt import methods
from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_page():
	"""Render a page that shows the user the title of the survey,
	   the instructions, and a button to start thr survey."""
	return render_template('start_page.html', satisfaction=satisfaction_survey)

