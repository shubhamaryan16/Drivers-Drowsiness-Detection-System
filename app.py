from flask import Flask, render_template
import subprocess
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start_detection():
    script_path = os.path.join(os.path.dirname(__file__), 'main.py')
    subprocess.Popen([sys.executable, script_path])
    return "Detection started. Check the webcam window."

if __name__ == '__main__':
    app.run(debug=True)
