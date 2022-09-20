from pyaxidraw import axidraw 
from flask import Flask, request

app = Flask(__name__)

@app.route('/api')
def hello():
  return 'Well hello there'

def process_json(content_type):
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

def get_pen_status():
    ad = axidraw.AxiDraw()
    ad.interactive()
    ad.connect()
    # Query machine pen state
    pen_up = ad.current_pen()
    ad.disconnect()
    return str(pen_up)

def get_device_name():
    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad.options.mode = 'manual'
    ad.options.manual_cmd = 'list_names'
    ad.plot_run()
    axidraw_list = ad.name_list
    return axidraw_list[0]

@app.route('/api/info', methods=['GET'])
def get_info():
  info_type = request.args.get('q')
  if (info_type == 'pen_state'):
    pen_up = get_pen_status()
    return {'penUp': pen_up}
  elif (info_type == 'device_name'):
    device_name = get_device_name()
    return {'deviceName': device_name}

@app.route('/api/command', methods=['POST'])
def run_command():
  content_type = request.headers.get('Content-Type')
  json = process_json(content_type)
  cmd = json.get('command')
  if (cmd == 'plot'):
    file_name = json.get('file_name')
    file_url = json.get('file_url')
    # plot(file_name, file_url)
    return {'command': cmd}
  elif (cmd == 'align'):
    # align_pen()
    return {'command': cmd}
  elif (cmd == 'toggle'):
    # toggle_pen()
    return {'command': cmd}
