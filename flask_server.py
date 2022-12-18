import os
import json
import re
import uuid
import datetime

from flask import Flask, render_template, request, make_response, session, redirect

import db_logic
from veksler_processor import process_veksler_form

server_object = Flask(__name__)
server_object.secret_key = 'abc'


@server_object.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@server_object.route('/veksler_start.html', methods=['GET', 'POST'])
def veksler():
    if request.method == 'GET':
        return render_template('veksler.html')


@server_object.route('/start.html', methods=['GET'])
def init_test():
    def get_json_q():
        with open('questioons_base.json') as f:
            q_base = json.load(f)
        return q_base

    if request.method == 'GET':
        session['points'] = 0
        session['user_name'] = str(uuid.uuid1())
        session['tasks'] = get_json_q()
        session['time_start'] = datetime.datetime.now(datetime.timezone.utc)
        session['time_last_q_started'] = datetime.datetime.now(
            datetime.timezone.utc)
        session['cur_section'] = 0
        session['is_trapped'] = False

        return redirect('/next_question.html')


@server_object.route('/next_question.html', methods=['GET'])
def show_question():
    if (session['time_last_q_started'] - session['time_start']).total_seconds() > 15*60 or session['tasks'][session['cur_section']] == []:
        return render_template('index.html')

    question = session['tasks'][session['cur_section']].pop(0)
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
        if time_current >= 32 or answer == False:
            type_action = 'stay_in_trap'
        else:
            type_action = 'from_trap'
            session['is_trapped'] = False
    else:
        if (datetime.datetime.now(datetime.timezone.utc) - session['time_last_q_started']).total_seconds() >= 32:
            session['is_trapped'] = True
            type_action = 'to_trap'
        elif answer == False:
            if session['points'] == 1:
                session['points'] = 0
            session['points'] -= 1
            print('очков сейчас', session['points'])
            type_action = 'stay_with_wrong_answer'
            if session['points'] == -2:
                if session['cur_section'] > 0:
                    type_action = 'down_section'
                session['cur_section'] = max(0, session['cur_section']-1)
                session['points'] = 0
        elif answer == True:
            if session['points'] == -1:
                session['points'] = 0
            session['points'] += 1
            print('очков сейчас', session['points'])
            type_action = 'stay_with_correct_answer'
            if session['points'] == 2:
                type_action = 'stay_in_the_last_section'
                if session['cur_section'] < 2:
                    type_action = 'up_section'
                session['cur_section'] = min(2, session['cur_section']+1)
                session['points'] = 0

    destination_index = session['cur_section']
    current_action_info = db_logic.record_users_action(user, time_current, type_action, source_index, destination_index)
    return 'ok'


@server_object.route('/veksler_result_processing', methods=['POST'])
def veksler_result_processing():
    print('##FOORM:', request.form)
    session['score'] = process_veksler_form(request.form)
    score = session['score'] 
    db_logic.set_user_level(session['user_name'], 1 if score <= 7 else 2 if score <= 14 else 3)
    return render_template('/show_veksler_results.html', score=score)


if __name__ == '__main__':
    server_object.run(debug=True)
