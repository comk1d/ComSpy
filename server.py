# flask_app.py
from flask import Flask, jsonify, request, render_template
import os
import json
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

LOG_DIR = "logs"

def load_user_logs(user_id):
    user_log_file = os.path.join(LOG_DIR, f"{user_id}.txt")
    logs = []

    if os.path.exists(user_log_file):
        with open(user_log_file, 'r') as file:
            for line in file:
                logs.append(json.loads(line.strip()))

    return logs

def load_user_logs_by_username(username):
    all_logs = []
    for filename in os.listdir(LOG_DIR):
        user_id = os.path.splitext(filename)[0]
        logs = load_user_logs(user_id)
        all_logs.extend([log for log in logs if log['user'] == username])
    return all_logs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs', methods=['GET'])
def get_logs():
    user_id = request.args.get('user_id')
    username = request.args.get('username')

    if user_id:
        logs = load_user_logs(user_id)
    elif username:
        logs = load_user_logs_by_username(username)
    else:
        logs = []

    return jsonify(logs)

@socketio.on('connect')
def handle_connect():
    emit('logs', [])

if __name__ == '__main__':
    socketio.run(app, debug=True)
