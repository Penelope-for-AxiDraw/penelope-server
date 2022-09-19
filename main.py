from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from pyaxidraw import axidraw 

app = FastAPI()

class Item(BaseModel):
  name: str
  price: float
  is_offer: Union[bool, None] = None


def get_pen_state():
    ad = axidraw.AxiDraw()
    ad.interactive()
    ad.connect()
    # Query machine pen state
    pen_up = ad.current_pen()
    ad.disconnect()
    return str(pen_up)


@app.get('/')
async def read_root():
  return {'Hello': 'World'}

@app.get('/items/{item_id}')
async def read_item(item_id: int, q: Union[str, None] = None):
  return {'item_id': item_id, 'q': q}

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
  return {'item_name': item.name, 'item_id': item_id}


@app.get('/info')
async def get_info(query: str):
  if (query == 'pen_state'):
    pen_up = get_pen_state()
    return {'penUp': pen_up}
  elif (query == 'device_name'):
    return {'deviceName': query}