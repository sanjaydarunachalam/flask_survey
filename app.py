from http.client import responses
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"
app = Flask(__name__)
app.config['SECRET_KEY']= "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECT'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Select survey"""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear session of responses"""

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response, redirect to next question"""

    #get response choice
    choice = request.form['answer']

    #adds response to session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses)==len(survey.questions)):

        #All questions answered
        return redirect("/complete")
    
    else:

        #Move on to next question
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    """show current question"""
    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        #acessed this page too soon before response key is populated
        return redirect("/")

    if(len(responses) == len(survey.questions)):
        #All questions answered. send to complete page
        return redirect("/complete")
    
    if(len(responses) != qid):
        #questions being acessed out of order
        flash(f"Invalid question id:{qid}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Survey complete, shows final page"""

    return render_template("completion.html")
    
    


        