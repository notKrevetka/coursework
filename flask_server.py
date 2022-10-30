from flask import Flask, render_template, request, make_response, session, redirect
# import db_logic
import os
import json
import re
import uuid

server_object = Flask(__name__)

@server_object.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method  == 'GET':
        return render_template('index.html')

@server_object.route('/start.html', methods=['GET', 'POST'])
def init_test():
    if request.method  == 'GET':
        session['points'] = 0
        session['user_name'] = uuid.uuid1()
        session['tasks'] = get_json_q()
        tasks = [set_1, set_2, set_3]
time_sum = 0
cur_section = 0
is_trapped = False

        return render_template('question_form.html')

if __name__ == '__main__':
    server_object.secret_key = 'abc'
    server_object.run(debug=True)
