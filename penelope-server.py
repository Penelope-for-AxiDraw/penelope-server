#!/usr/bin/env python


# + + + + + + + + + + + + + + + +
# Receive data from a browser via WebSocket

import asyncio
import json
from pyaxidraw import axidraw 
import requests
import subprocess
import websockets

print("Ready to receive AxiDraw commands via WebSocket")

# ADDR = '10.0.1.19'
# NOTE: This 'hostname -I' might not work on MacOS?
temp = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE, encoding='utf-8')
ADDR = temp.stdout.split(' ')[0]
PORT = 5678

# Local folder to save data
local_folder = 'files/'

def get_file(remote_url, file_name):
  # Make http request for remote file data
  data = requests.get(remote_url + file_name)
  if(data.status_code == 404):
    print('Something went wrong')
  else:
    # Save file data to local copy
    with open(local_folder + file_name, 'wb') as file:
      file.write(data.content)
      # print('Downloaded the file')

def axi_plot(file):
  print('Plotting with AxiDraw!')
  ad = axidraw.AxiDraw()
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

async def listen_messages(websocket):
    while True:
        msg = await websocket.recv()
        await websocket.send(json.dumps({'greeting': 'Hi, received your command.'}))
        if (msg == 'get_name'):
            try:
                device_name = get_name()
                status = json.dumps({'deviceName': device_name})
            except:
                status = json.dumps({'deviceName': 'no device name'})
            await websocket.send(status)
        elif (msg == 'get_pen_state'):
            # device_name = get_name()
            pen_up = get_pen_state()
            status = json.dumps({'penUp': pen_up})
            await websocket.send(status)
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

async def main():
    async with websockets.serve(listen_messages, ADDR, PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())
