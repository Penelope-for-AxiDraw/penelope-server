<img width="143" alt="penelope-logo@2x" src="https://user-images.githubusercontent.com/10648307/189042884-1d4daf88-a954-47db-9e78-a628f45ece93.png">

Welcome to the companion backend for <a href="https://github.com/Penelope-for-AxiDraw/penelope" target="_blank">Penelope</a>. This super-basic server acts as a bridge between the web app and an <a href="https://shop.evilmadscientist.com/productsmenu/846" target="_blank">AxiDraw pen plotter</a>. To plot SVG images to a connected AxiDraw, Penelope Server and web app should be running on the same machine.

### Running the App

This project requires Python 3 and has <a href="https://axidraw.com/doc/py_api/#" target="_blank">`py-axidraw`</a>, `requests` and `websockets` as dependencies. First, download/clone this repo to your computer. Then, install your dependencies via commmand line:

```bash
$ python -m pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip
$ pip install requests
$ pip install websockets
```

Although not required, it might be useful to install these libraries to a <a href="https://docs.python.org/3/tutorial/venv.html" target="_blank">Python virtual environment</a>. Once the dependencies are installed, you can run the app from the command line. From the server's directory:

```bash
$ python penelope-server.py
```

At this point, the server will wait for commands sent via WebSocket from your locally-running Penelope web app.

### Development
In its current state, this app incorporates just a few methods from the <a href="https://axidraw.com/doc/py_api/#introduction" target="_blank">AxiDraw Python API</a>. You can of course modify the existing methods in the server. Better yet, you could add functionality to the server _and_ the web app to leverage more features of the AxiDraw Python API. As an example, the API has methods for <a href="https://axidraw.com/doc/py_api/#speed_pendown" target="_blank">adjusting pen speed</a> and/or plotting <a href="https://axidraw.com/doc/py_api/#copies" target="_blank">multiple copies</a> of your SVG artwork. You could add UI elements to the web app that allow you to control these plotting properties. The sky's the limit 🚀
