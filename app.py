from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

INVALID_QUESTION_MSG = 'You attempted to access an invalid question!'

RESPONSES_KEY = 'responses'

@app.route('/')
def start_page():
	"""Render a page that shows the user the title of the survey,
	   the instructions, and a button to start thr survey."""
	return render_template('start_page.html', survey=survey)

@app.route('/begin', methods=['POST'])
def start_survey():
	"""Initialize the session by setting session['responses'] to an empty list."""
	responses = []
	session[RESPONSES_KEY] = responses
	return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def handle_question(qid):
	"""Show a form asking the question and listing the choices as radio buttons."""
	responses = session[RESPONSES_KEY]
	if len(responses) < len(survey.questions):
		if qid == len(responses):
			return render_template('show_question_page.html', question_num=qid, survey=survey)
		flash(INVALID_QUESTION_MSG)
		return redirect(f'/questions/{len(responses)}')
	return render_template('/thankyou.html', survey=survey)

@app.route('/answer', methods=['POST'])
def handle_answer():
	"""Append the answer to the responses list and redirect the user to the next question.
	   If the answer is to the last question, redirect them to a simple 'Thank You' page"""
	answer = request.form['answer']
	responses = session[RESPONSES_KEY]
	responses.append(answer)
	session[RESPONSES_KEY] = responses
	qid = int(request.form['qid']) + 1
	if qid < len(survey.questions):
		return redirect(f'/questions/{qid}')
	return render_template('/thankyou.html', survey=survey)