#!/usr/bin/env python

import json
from pyaxidraw import axidraw 
import requests
from constants import PORT, LOCAL_FOLDER, MSG


# + + + + + + + + + + + + + + + +

# ADDRESS = ADDR if ADDR.endswith('.local') else '{}.local'.format(ADDR)

def get_file(remote_url, file_name):
  # Make http request for remote file data
  data = requests.get(remote_url + file_name)
  if(data.status_code == 404):
    print(MSG['OHNO'])
  else:
    # Save file data to local copy
    with open(LOCAL_FOLDER + file_name, 'wb') as file:
      file.write(data.content)


def axi_plot(file_name):
  print(MSG['PLOTTING'])
  ad = axidraw.AxiDraw()
  ad.plot_setup(LOCAL_FOLDER + file_name)
  ad.options.speed_pendown = 24
  ad.options.reordering = 1
  ad.plot_run()


def run_mode(mode):
    print(mode)
    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad.options.mode = mode
    ad.plot_run()


def get_pen_status():
    ad = axidraw.AxiDraw()
    ad.interactive()
    ad.connect()
    # Query machine pen state
    pen_up = ad.current_pen()
    ad.disconnect()
    return str(pen_up)


def get_device_name():
    device_name = 'no device name'
    try:
      ad = axidraw.AxiDraw()
      ad.plot_setup()
      ad.options.mode = 'manual'
      ad.options.manual_cmd = 'list_names'
      ad.plot_run()
      axidraw_list = ad.name_list
      device_name = axidraw_list[0]
    except:
      pass

    return device_name

