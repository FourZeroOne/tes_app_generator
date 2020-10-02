import logging
from src.utils.lambda_proxy import API

from src.app_base import ROUTES
from src.config import CONFIG


class RequestData():
    def __init__(self):
        self.args = {}
        self.data = '{}'
        self.remote_addr = ''
        self.headers = {}


FORMAT = """--------------------------------------------------------------------------------
[%(asctime)s] {%(pathname)s:%(lineno)d}
%(levelname)s - %(message)s
--------------------------------------------------------------------------------"""
logging.basicConfig(level=logging.WARNING, format=FORMAT)

api_app = API(name="app")

for route in ROUTES:
    api_app._add_route(
        route['url'],
        route['endpoint'],
        methods=route['methods'],
        cors=True,
        data={
            'auth_required': route['auth_required'],
            'request_obj': RequestData(),
            'app_type': 'lambda_proxy',
            'secret_key': CONFIG.get('secret_key')
            }
    )

