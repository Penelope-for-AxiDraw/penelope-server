from pyaxidraw import axidraw 
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import axi_plot, get_device_name, get_file, get_pen_status, run_mode
from constants import ALIGN, TOGGLE, MSG

app = Flask(__name__)
CORS(app)

def process_json(content_type):
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'


# ROUTES -----------------------

@app.route('/api')
def hello():
  return jsonify({'message': MSG['HELLO']})

@app.route('/api/info')
def get_info():
  info_type = request.args.get('q')
  if (info_type == 'penState'):
    pen_up = get_pen_status()
    return jsonify({'penUp': pen_up})
  elif (info_type == 'deviceName'):
    device_name = get_device_name()
    return jsonify({'deviceName': device_name})

@app.route('/api/command', methods=['POST'])
def run_command():
  content_type = request.headers.get('Content-Type')
  json = process_json(content_type)
  cmd = json.get('action')
  OK = jsonify({'command': cmd, 'message': 'OK'})
  if (cmd == 'plot'):
    file_name = json.get('fileName')
    file_url = json.get('fileUrl')
    get_file(file_url, file_name)
    axi_plot(file_name)
    return OK
  elif (cmd == ALIGN):
    run_mode(ALIGN)
    return OK
  elif (cmd == TOGGLE):
    run_mode(TOGGLE)
    return OK
