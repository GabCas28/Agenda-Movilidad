from flaskwebgui import FlaskUI
from main.wsgi import application

FlaskUI(application, port=8000).run()