<img width="143" alt="penelope-logo@2x" src="https://user-images.githubusercontent.com/10648307/189042884-1d4daf88-a954-47db-9e78-a628f45ece93.png">

Welcome to the companion backend for <a href="https://github.com/Penelope-for-AxiDraw/penelope" target="_blank">Penelope</a>. This super-basic server acts as a bridge between the web app and an <a href="https://shop.evilmadscientist.com/productsmenu/846" target="_blank">AxiDraw pen plotter</a>. To plot SVG images to a connected AxiDraw, Penelope Server and the web app should be running on the same machine.

### Running the App

This project requires Python 3 and has <a href="https://axidraw.com/doc/py_api/#" target="_blank">`py-axidraw`</a>, <a href="https://flask.palletsprojects.com/en/2.2.x/" target="_blank">`flask`</a>, <a href="https://flask-cors.readthedocs.io/en/latest/" target="_blank">`Flask-CORS`</a> and <a href="https://pypi.org/project/requests/" target="_blank">`requests`</a> as dependencies. First, download/clone this repo to your computer. Then, install your dependencies via commmand line:

```bash
$ python -m pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip
$ python -m pip install requests
$ pip install Flask
$ pip install -U flask-cors
```

Although not required, it might be useful to install these libraries to a <a href="https://docs.python.org/3/tutorial/venv.html" target="_blank">Python virtual environment</a>. Once the dependencies are installed, you can run the app from the command line. From the server's directory:

```bash
$ flask --app pen_api run --host=127.0.0.1 --port=5000
```

The host in the above case `127.0.0.1` is the default host of your locally-running Penelope web app. At this point, the server is ready to receive API calls via port 5000. If you need to change the port, you'll need to update it in the above `flask run` command and inside the <a href="https://github.com/Penelope-for-AxiDraw/penelope/blob/main/src/constants/index.ts" target="_blank">NextJS app</a>.

### Development
In its current state, this app incorporates just a few methods from the <a href="https://axidraw.com/doc/py_api/#introduction" target="_blank">AxiDraw Python API</a>. You can of course modify the existing methods in the server. Better yet, you could add functionality to the server _and_ the web app to leverage more features of the AxiDraw Python API. As an example, the API has methods for <a href="https://axidraw.com/doc/py_api/#speed_pendown" target="_blank">adjusting pen speed</a> and/or plotting <a href="https://axidraw.com/doc/py_api/#copies" target="_blank">multiple copies</a> of your SVG artwork. You could add UI elements to the web app that allow you to control these plotting properties. The sky's the limit 🚀
