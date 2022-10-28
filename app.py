from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.debug=True

debug = DebugToolbarExtension(app)


@app.route('/')
def show_home():
    """Shows homepage"""
    return render_template('home.html')

@app.route('/questions/<int:number>')
def show_question(number):
    responses = session['responses']
    if number != len(responses):
        flash('You are trying to access an invalid question')
        return redirect(f'/questions/{len(responses)}')
    if number == len(survey.questions):
        return redirect ('/thankyou')
    question = survey.questions[number]
    return render_template ('question.html', num=number, question=question)

@app.route('/answer/<int:number>', methods =['GET','POST'])
def answer_question(number):
    """records answer question and redirects user"""
    response = request.args.get('response')
    responses = session['responses']
    responses.append(response)
    print(session['responses'])
    session['responses']=responses
    new_num = number + 1
    return redirect(f'/questions/{new_num}')

@app.route('/thankyou')
def thank_user():
    """Thanks user for completing the survey"""
    return render_template ('thankyou.html')

@app.route('/create_response_list',methods=['GET','POST'])
def create_response_list():
    session['responses'] = []
    return redirect('/questions/0')