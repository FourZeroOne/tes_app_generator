from tes.config import CONFIG
from tes.api import API


if CONFIG is None:
    raise Exception('ERROR: Could not get configs.')

API.app_db.connect(CONFIG.get('db_uri'))
API.app_db.set_db_auth('_malin')

from . import resources
