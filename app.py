from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []

@app.route('/')
def show_survey_start():
    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods=['GET'])
def start_survey():

    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_questions():

    choice = request.form['answer']

    responses.append(choice)

    return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:qid>')
def show_questions(qid):
    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    if (len(responses) != qid):
        flash(f"Trying to access an invalid question.")
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[qid]
    return render_template(
        'question.html', question_num=qid, question=question)
    
@app.route('/complete')
def complete_survey():
    return render_template('complete.html')