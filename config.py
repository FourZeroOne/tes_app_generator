import os
from confighandler import ConfigHandler

if os.path.exists('settings.json') and os.path.exists('settings_default.json'):
    CONFIG =  ConfigHandler('settings.json', os.environ, 'settings_default.json')
else:
    CONFIG =  ConfigHandler(os.environ)
