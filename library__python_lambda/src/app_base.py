# import mongoengine
import sentry_sdk
#from pymongo import read_preferences
from .config import CONFIG

from .resources.example import ROUTES as example_routes

if CONFIG.get('sentry'):
    sentry_sdk.init(CONFIG.get('sentry'))

"""
db_con = mongoengine.connect(
    alias='default', host=CONFIG.get('db_uri'),
    read_preference=read_preferences.ReadPreference.PRIMARY)

mongoengine.connection.SWITCH_DB_ALLOWED = True
"""

ROUTES = []
ROUTES.extend(example_routes)
