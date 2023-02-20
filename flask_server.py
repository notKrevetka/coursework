import os
import json
import re
import uuid
import datetime

from flask import Flask, render_template, request, make_response, session, redirect

import db_logic

server_object = Flask(__name__)
server_object.secret_key = b'abc'

@server_object.route('/', methods=['GET', 'POST'])
@server_object.route('/index.html', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')


@server_object.route('/start.html', methods=['POST'])
def init_test():
    def get_json_q():
        with open('questioons_base.json') as f:
            q_base = json.load(f)
        return q_base

    if request.method == 'POST':
        session['points'] = 0
        session['user_name'] = request.form['surname'] + str(uuid.uuid4())
        session['tasks'] = get_json_q()
        session['time_start'] = datetime.datetime.now(datetime.timezone.utc)
        session['time_last_q_started'] = datetime.datetime.now(datetime.timezone.utc)
        session['cur_section'] = 0
        session['is_trapped'] = False
        return redirect('/next_question.html')


@server_object.route('/next_question.html', methods=['GET'])
def show_question():
    if (session['time_last_q_started'] - session['time_start']).total_seconds() > 15*60 or session['tasks'][session['cur_section']%5] == []:
        return redirect('/ending.html')

    question = session['tasks'][session['cur_section']%5].pop(0)
    print('Выдергнут вопрос:', question)

    session['time_last_q_started'] = datetime.datetime.now(
        datetime.timezone.utc)
    return render_template('question_form.html', question=question)


@server_object.route('/send_answer', methods=['POST'])
def send_answer():
    user, time_current, type_action, source_index, destination_index = session['user_name'], (datetime.datetime.now(
        datetime.timezone.utc) - session['time_last_q_started']).total_seconds(), None, session['cur_section'], None
    answer = request.form['answer'] == "true"
    if session['is_trapped']:
        if time_current >= 31 or answer == False:
            type_action = 'in_trap'
        else:
            type_action = 'from_trap'
            session['cur_section'] -= 5
            session['is_trapped'] = False
    else:
        if (datetime.datetime.now(datetime.timezone.utc) - session['time_last_q_started']).total_seconds() >= 31:
            session['is_trapped'] = True
            session['cur_section'] += 5
            type_action = 'to_trap'

        elif answer == False:
            if session['points'] == 1:
                session['points'] = 0
            session['points'] -= 1
            type_action = 'wrong_answer'



        elif answer == True:
            if session['points'] < 0:
                session['points'] = 0
            session['points'] += 1
            # print('очков сейчас', session['points'])
            type_action = 'correct_answer'
            if session['points'] == 2:
                type_action = 'correct_answer'
                if session['cur_section'] < 4:
                    type_action = 'up_section'
                session['cur_section'] = min(4, session['cur_section']+1)
                session['points'] = 0

    destination_index = session['cur_section']
    current_action_info = db_logic.record_users_action(user, time_current, type_action, source_index, destination_index)
    return 'ok'

@server_object.route('/ending.html', methods=['GET', 'POST'])
def final_page():
    return render_template('/ending.html')

if __name__ == '__main__':
    server_object.run(debug=True)
