# -*- coding: utf-8 -*-
#!/usr/bin/env python
import random
from threading import Lock
from flask import *
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from database import *
import os
from werkzeug.utils import secure_filename


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/upload/<name>', methods=['POST', 'GET'])
def upload(name):
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save('static/file/'+filename)
        file_path(name, filename)
        return redirect('/'+filename)
    return render_template('file.html', name=name)


@app.route('/')
def index():
    a = str(random.randint(0, 10000))
    return redirect(a)


@app.route('/<name>')
def notepage(name):
    a = find(name)
    if a:
        if a['password']:
            return render_template('pwd.html', name=name)
        else:
            if a['path']:
                return render_template('index.html', name=a['name'], data=a['data'], path=['path'])
            else:
                return render_template('index.html', name=a['name'], data=a['data'])
    else:
        return render_template('index.html', name=name)


@app.route('/<name>/file')
def download(name):
    ans = find(name)
    return redirect(url_for('static', filename='file/' + ans['path']))


@app.route('/login', methods=['POST'])
def verify():
    if request.method == 'POST':
        a = find(request.form['name'])
        if a['password'] == request.form['password']:
            return render_template('index.html', name=a['name'], data=a['data'])
        else:
            return redirect('/' + request.form['name'])
    else:
        abort(401)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    add(message['name'], message['data'])
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('password', namespace='/test')
def password(pwds):
    session['receive_count'] = session.get('receive_count', 0) + 1
    pwd(pwds['name'], pwds['data'])
    emit('my_response',
         {'data': pwds['name'] + " has a password now.", 'count': session['receive_count']})


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('connect', namespace='/test')
def test_connect():
    #global thread
    #with thread_lock:
    #    if thread is None:
    #        thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)