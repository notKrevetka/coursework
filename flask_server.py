from flask import Flask, render_template, request, make_response, session, redirect
# import db_logic
import os
import json
import re
import uuid
import datetime 

server_object = Flask(__name__)

@server_object.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method  == 'GET':
        return render_template('index.html')

@server_object.route('/start.html', methods=['GET', 'POST'])
def init_test():
    def get_json_q():
        with open('questioons_base.json') as f:
            q_base = json.load(f)
        return q_base
    
    if request.method  == 'GET':
        session['points'] = 0
        session['user_name'] = uuid.uuid1()
        session['tasks'] = get_json_q()
        session['time_start'] = datetime.datetime.now(datetime.timezone.utc)
        session['time_last_q_started'] = datetime.datetime.now(datetime.timezone.utc)
        session['cur_section'] = 0
        session['is_trapped'] = False
        
        return redirect('/next_question.html')



@server_object.route('/next_question.html', methods=['GET', 'POST'])
def show_question():
    if request.method  == 'GET':
        print('дай вопрос из секции номер', session['cur_section'])
        if (session['time_last_q_started'] - session['time_start']).total_seconds() > 15*60 or session['tasks'][ session['cur_section']] == []:
            return render_template('index.html')

        question = session['tasks'][session['cur_section']].pop(0)
        session['time_last_q_started'] = datetime.datetime.now(datetime.timezone.utc)
        print(question, session['cur_section'] )
        return render_template('question_form.html', question=question)
    if request.method  == 'POST':
        print('пришел ответ для вопроса из секции номер', session['cur_section'])
        answer = request.form['answer'] == "true"
        print(session['is_trapped'], bool(answer), session['cur_section'])
        if session['is_trapped']:
            if  (datetime.datetime.now(datetime.timezone.utc) - session['time_last_q_started']).total_seconds() >= 32 or answer==False:
                pass
            else:
                print('вышел из ловушки', session['cur_section'], datetime.datetime.now(datetime.timezone.utc) -session['time_start'] )
                session['is_trapped'] = False
        else:
            if (datetime.datetime.now(datetime.timezone.utc) - session['time_last_q_started']).total_seconds() >= 32:
                session['is_trapped'] = True
                print('пошел в ловушку',  session['cur_section'], datetime.datetime.now(datetime.timezone.utc) -session['time_start'] )
            elif answer == False:
                session['points'] -= 1
                if  session['points'] == -3:
                    if session['cur_section'] > 0:
                        print('понижение секции' ,session['cur_section'], "->",session['cur_section']-1,  datetime.datetime.now(datetime.timezone.utc) -session['time_start'] )
                    session['cur_section'] = max(0, session['cur_section']-1)
                    session['points'] = 0
            elif answer == True:
                if session['cur_section'] < 2:
                    print('up секции' ,session['cur_section'], "->",session['cur_section']+1,  datetime.datetime.now(datetime.timezone.utc) -session['time_start'] )
                session['cur_section'] = min(2, session['cur_section']+1)
                session['points'] = 0
        print(session['is_trapped'], answer, session['cur_section'])
        return 'ПОМОГИТИ ПОЖАЛУЙСТА'









if __name__ == '__main__':
    server_object.secret_key = 'abc'
    server_object.run(debug=True)
