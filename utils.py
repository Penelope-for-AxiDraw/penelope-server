#!/usr/bin/env python

import json
from pyaxidraw import axidraw 
import requests
from constants import LOCAL_FOLDER, MSG


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
  webhook_url = get_notify()
  if(webhook_url):
    ad.options.webhook = True
    ad.options.webhook_url = webhook_url
  ad.plot_run()


def run_mode(mode):
    print(mode)
    ad = axidraw.AxiDraw()
    ad.plot_setup()
    ad.options.mode = mode
    ad.plot_run()


def get_pen_status():
    pen_up = 'None'
    try:
      ad = axidraw.AxiDraw()
      ad.interactive()
      ad.connect()
      # Query machine pen state
      pen_up = ad.current_pen()
      ad.disconnect()
    except:
      pass
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

'''
We can use AxiDraw's built-in support for webhooks in order to receive notifications
when plotting is complete. First you'll need to use a third-party service to create a
webhook. Then, paste its URL into the 'webhook_base_url' field in config.json. (This
repo includes an example config file for reference). For information about how to
create a webhook with IFTTT, check out https://wiki.evilmadscientist.com/Webhooks.
'''
def get_notify():
  config_filename = 'config.json'
  try:
    with open(config_filename, 'r') as config_file:
      info = json.load(config_file)
  except:
    return None

  if 'webhook_base_url' in info.keys():
    return info['webhook_base_url']

  return None