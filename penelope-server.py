#!/usr/bin/env python


# + + + + + + + + + + + + + + + +
# Receive data from a browser via WebSocket

import asyncio
import datetime
import websockets
import requests
import json
import colorsys
import sys
from pyaxidraw import axidraw 

print("Ready to receive AxiDraw commands via WebSocket")

# ADDR = 'localhost'
ADDR = '10.0.1.25'
PORT = 5678

# Local folder to save data
local_folder = 'files/'

# Remote location of file to retrieve
root_url = 'https://gist.githubusercontent.com/'
content_path = 'computershawn/f8c1892bbf88a4b70924121f51df58ee/raw/d284d74c9e1473b1a87305fc3bd3aa94d160bb87/'

def get_file(remote_url, file_name):
  # Make http request for remote file data
  data = requests.get(remote_url + file_name)
  if(data.status_code == 404):
    print('Something went wrong')
  else:
    # Save file data to local copy
    with open(local_folder + file_name, 'wb') as file:
      file.write(data.content)
    print('Downloaded the file')

def axi_plot(file):
  print('Plotting with AxiDraw!')
  ad = axidraw.AxiDraw()
  # ad.plot_setup()
  ad.plot_setup(local_folder + file)
  ad.options.speed_pendown = 12
  ad.options.reordering = 1
  ad.plot_run()

def run_mode(mode):
    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad.options.mode = mode
    ad.plot_run()

def get_name():
    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad.options.mode = "manual"
    ad.options.manual_cmd = "list_names"
    ad.plot_run()
    axidraw_list = ad.name_list
    return axidraw_list[0]

def get_pen_state():
    ad = axidraw.AxiDraw()
    ad.interactive()
    ad.connect()
    # Query machine pen state
    pen_up = ad.current_pen()
    ad.disconnect()
    return str(pen_up)

async def listen_messages(sock, path):
    while True:
        msg = await sock.recv()
        await sock.send(json.dumps({'greeting': 'Hi, received your command.'}))
        if (msg == 'get_name'):
            device_name = get_name()
            status = json.dumps({'deviceName': device_name})
            await sock.send(status)
        elif (msg == 'get_pen_state'):
            # device_name = get_name()
            pen_up = get_pen_state()
            status = json.dumps({'penUp': pen_up})
            await sock.send(status)
        else:
            try:
                process_command(msg)

            except (ValueError, KeyError, TypeError):
                print("Data format error")

def process_command(message):
    cmd = message.split('|')
    action = cmd[0]

    if(action == 'toggle'):
        run_mode('toggle')
    
    if(action == 'align'):
        run_mode('align')
    
    if(action == 'plot'):
        file_url = cmd[1]
        file_name = cmd[2]
        get_file(file_url, file_name)
        axi_plot(file_name)


start_server = websockets.serve(listen_messages, ADDR, PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

