#!/usr/bin/env python

import platform

ADDR = platform.node()
PORT = 5678
LOCAL_FOLDER = 'files/'
MSG = {
  'FORMAT_ERROR': 'Data format error',
  'GREET': 'Ready to receive AxiDraw commands |',
  'HELLO': 'Well hello there, this is the Penelope API',
  'OHNO': 'Something went wrong',
  'PLOTTING': 'Plotting with AxiDraw!'
}
TOGGLE = 'toggle'
ALIGN = 'align'