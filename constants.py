#!/usr/bin/env python

import platform

ADDR = platform.node()
PORT = 5678
LOCAL_FOLDER = 'files/'
MESSAGES = {
  'GREET': 'Ready to receive AxiDraw commands |',
  'OHNO': 'Something went wrong',
  'PLOTTING': 'Plotting with AxiDraw!',
  'FORMAT_ERROR': 'Data format error'
}
