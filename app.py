from crypt import methods
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

INVALID_QUESTION_MSG = 'You attempted to access an invalid question.'

responses = []

@app.route('/')
def start_page():
	"""Render a page that shows the user the title of the survey,
	   the instructions, and a button to start thr survey."""
	return render_template('start_page.html', satisfaction=satisfaction_survey)

@app.route('/questions/<question>')
def handle_question(question):
	"""Show a form asking the question and listing the choices as radio buttons."""
	if len(responses) < len(satisfaction_survey.questions):
		if int(question) == len(responses):
			return render_template('show_question_page.html', question=int(question), satisfaction=satisfaction_survey)
		flash(INVALID_QUESTION_MSG)
		return redirect(f'/questions/{len(responses)}')
	return render_template('/thankyou.html', satisfaction=satisfaction_survey)

@app.route('/answer', methods=['POST'])
def handle_answer():
	"""Append the answer to the responses list and redirect the user to the next question.
	   If the answer is to the last question, redirect them to a simple 'Thank You' page"""
	answer = request.form['answer']
	responses.append(answer)
	question = int(request.form['question']) + 1
	if question < len(satisfaction_survey.questions):
		return redirect(f'/questions/{question}')
	return render_template('/thankyou.html', satisfaction=satisfaction_survey)

	