from flaskwebgui import FlaskUI
from main.wsgi import application

FlaskUI(app=application, server='django', port=8000).run()