from flask import *
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# app.run(host='192.168.0.2', port=5000, debug=False, threaded=True)
# app.debug = True

from app import routes


