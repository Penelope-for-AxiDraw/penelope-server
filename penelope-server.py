#!/usr/bin/env python


# + + + + + + + + + + + + + + + +
# Receive data from a browser via WebSocket

import asyncio
import json
from pyaxidraw import axidraw 
import requests
import websockets
from constants import ADDR, PORT, LOCAL_FOLDER, MESSAGES

ADDRESS = ADDR if ADDR.endswith('.local') else '{}.local'.format(ADDR)

greeting = 'Ready to receive AxiDraw commands via WebSockets |'
print(f"{MESSAGES['GREET']} {ADDRESS}:{PORT}")

def get_file(remote_url, file_name):
  # Make http request for remote file data
  data = requests.get(remote_url + file_name)
  if(data.status_code == 404):
    print(MESSAGES['OHNO'])
  else:
    # Save file data to local copy
    with open(LOCAL_FOLDER + file_name, 'wb') as file:
      file.write(data.content)
      # print('Downloaded the file')

def axi_plot(file):
  print(MESSAGES['PLOTTING'])
  ad = axidraw.AxiDraw()
  ad.plot_setup(LOCAL_FOLDER + file)
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
            device_name = 'no device name'
            try:
                device_name = get_name()
            except:
                pass
            finally:
                status = json.dumps({'deviceName': device_name})

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
                print(MESSAGES['FORMAT_ERROR'])

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
    async with websockets.serve(listen_messages, ADDRESS, PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())
