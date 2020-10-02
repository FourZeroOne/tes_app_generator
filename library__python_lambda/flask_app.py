import logging
from flask import Flask, request
from flask_cors import CORS

from src.app_base import ROUTES
from src.config import CONFIG

FORMAT = """--------------------------------------------------------------------------------
[%(asctime)s] {%(pathname)s:%(lineno)d}
%(levelname)s - %(message)s
--------------------------------------------------------------------------------"""
logging.basicConfig(level=logging.WARNING, format=FORMAT)

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

cors = CORS(app, resources={r"*": {"origins": "*"}}, max_age=300)


for route in ROUTES:
    app.add_url_rule(
        route['url'],
        route['name'],
        route['endpoint'],
        methods=route['methods'],
        defaults={'data': {
            'auth_required': route['auth_required'],
            'request_obj': request,
            'app_type': 'flask',
            'secret_key': CONFIG.get('secret_key')
            }
        }
    )
