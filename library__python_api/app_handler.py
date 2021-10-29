from tes.config import CONFIG

from src import app_base

if CONFIG.get('app_type') == 'flask':
    from tes.api.flask import *
else:
    from tes.api.aws_lambda import *
