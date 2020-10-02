import json

from datetime import datetime

from ..utils.request_handler import RequestArgs, RequestHandler


def examples(data):
    request_obj = RequestHandler(data)
    args = RequestArgs(request_obj.args)

    return json.dumps({}, default=str), 200


ROUTES = [
    {
        'url': '/examples',
        'name': 'examples__examples',
        'endpoint': examples,
        'methods': ['GET'],
        'auth_required': False
    }
]
