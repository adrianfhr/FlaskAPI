import os

from flask import Flask
from dotenv import load_dotenv

from api.views import blueprint
from config import Config
from extensions import db

load_dotenv()

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config.from_object(Config)

db.init_app(app)

if __name__ == '__main__':
    app.run(
        host=app.config.get('FLASK_HOST'),
        port=app.config.get('FLASK_PORT'),
        debug=app.config.get('FLASK_DEBUG')
    )