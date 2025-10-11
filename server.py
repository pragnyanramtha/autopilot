from flask import Flask, request
from flask_socketio import SocketIO
import subprocess
import os
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def stream_output(pipe, sid):
    try:
        for line in iter(pipe.readline, b''):
            socketio.emit('terminal_output', {'output': line.decode('utf-8')}, room=sid)
    except Exception as e:
        print(f"Error streaming output: {e}")
    finally:
        pipe.close()

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Start a new cli.py process for each client
    cmd = ['python', '-u', 'cli.py']
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    env['PYTHONUTF8'] = '1'
    env['GEMINI_API_KEY'] = 'AIzaSyBXU-eQd5HOeIm2IpAaMTTS1MgbKGB08v4'
    env['NO_RICH'] = '1'
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    # Store the process and streams in the session
    # This is a simplified approach; for production, you'd need a more robust way to manage sessions
    # from flask import request; request.sid
    sid = request.sid
    socketio.server.enter_room(sid, sid)
    socketio.server.save_session(sid, {'process': process})

    # Start threads to stream stdout and stderr
    stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, sid))
    stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, sid))
    stdout_thread.start()
    stderr_thread.start()

@socketio.on('terminal_input')
def handle_terminal_input(data):
    sid = request.sid
    session = socketio.server.get_session(sid)
    process = session.get('process')
    if process and process.poll() is None:
        try:
            process.stdin.write((data['input'] + '\n').encode('utf-8'))
            process.stdin.flush()
        except Exception as e:
            print(f"Error writing to stdin: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    sid = request.sid
    session = socketio.server.get_session(sid)
    process = session.get('process')
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
        except Exception as e:
            print(f"Error terminating process: {e}")
            process.kill()
        socketio.server.close_room(sid, sid)

if __name__ == '__main__':
    socketio.run(app, port=5000)