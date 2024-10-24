import subprocess
from flask import Flask, render_template
import os

app = Flask(__name__)

script_process = None

@app.route('/')
def index():
    global script_process
    if script_process is None or script_process.poll() is not None:
        script_process = subprocess.Popen(['python', 'main.py'])
    return render_template('index.html')

if __name__ == '__main__':
    try:
        app.run(debug=True, host='127.0.0.1', port=5002)
    finally:
        if script_process is not None:
            script_process.terminate()