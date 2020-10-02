import os
import pathlib
import sys
import shutil

from datetime import datetime

from jinja2 import Template
from confighandler import ConfigHandler

app = {}

lib_type = input('Type [python_lib]: ') or 'python_lib'

app['name'] = input('Name*: ')
app['short_description'] = input('Short Description: ')
app['keywords'] = input('Keywords: ')
app['author'] = input(
    'Author [Johannes Eimer Production (JEP)]: ') or 'Johannes Eimer Production (JEP)'
app['author_email'] = input(
    'Author Email [info@jep-dev.com]: ') or 'info@jep-dev.com'
app['license_type'] = input('License [MIT]: ') or 'MIT'
target_folder = input('Generation Target Folder [../gen/]: ') or '../gen/'

if app['name'] == '':
    print('App name is empty. Please try again.')
    sys.exit('App name is empty. Please try again.')


class TemplateHandler:
    def render_string(self, content, *args, **kwargs):
        tm = Template(content)
        return tm.render(*args, **kwargs)


class StaticHandler:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def get_file(self, *args):
        path = os.path.join(self.base_dir, 'static', *args)
        content = ''

        if not os.path.isfile(path):
            raise Exception('Could not find static file.', path)

        with open(path, 'r') as f:
            content = f.read()
        return content


class Library:
    def __init__(self, base_dir, lib_name):
        self.app = None
        self.lib_name = lib_name
        self.base_dir = base_dir
        self.static_handler = StaticHandler(self.base_dir)
        self.template_handler = TemplateHandler()
        self.force_overwrite = False
        self.config = ConfigHandler(self.get_conf_path())

    def exists(self):
        for file_name in os.listdir(self.base_dir):
            if file_name == 'library__' + self.lib_name:
                return True
        return False

    def get_lib_path(self):
        return os.path.join(self.base_dir, 'library__' +
                            self.lib_name)

    def get_conf_path(self):
        path = os.path.join(self.get_lib_path(), 'parse_settings.json')

        if not os.path.isfile(path):
            raise Exception('Could not find parse_settings.json file.', path)

        return path

    def create_folder(self, *args):
        target = os.path.join(*args)
        if os.path.isdir(target):
            return True
        os.makedirs(target, exist_ok=True)
        return True

    def create_file(self, content, *args):
        target = os.path.join(*args)

        with open(target, 'w+') as f:
            f.seek(0)
            f.write(content)
            f.truncate()
        return True

    def copy_lib_to_target(self, target_path, source_path):
        target = os.path.join(target_path, self.app['name'])
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(source_path, target)
        return True

    def parse_file(self, *args):
        target = os.path.join(*args)
        if not os.path.exists(target):
            return False

        with open(target, 'r+') as f:
            content = f.read()
            f.seek(0)
            f.write(
                self.template_handler.render_string(
                    content,
                    app=app,
                    current_year=datetime.utcnow().year)
                )
            f.truncate()
        return True

    def remove_file(self, *args):
        target = os.path.join(*args)
        if os.path.exists(target):
            os.remove(target)
        return True

    def generate(self, app, target_folder):
        self.app = app
        self.target_folder = target_folder

        source = self.get_lib_path()

        # check if lib exists
        if not self.exists():
            raise Exception('Could not find lib.', self.lib_name)

        # rendering
        ## license - get
        self.app['license_content'] = self.template_handler.render_string(
            self.static_handler.get_file(
                'license', self.app['license_type']),
            app=app, current_year=datetime.utcnow().year)

        # check if lib already exists
        if os.path.exists(os.path.join(self.target_folder, self.app['name'])):
            overwrite_app = input('App {0} already exists. Do you want to overwrite it? (y/N): '.format(self.app['name'])) or 'n'
            if overwrite_app.upper() == 'N':
                return False

        # create file structure
        self.copy_lib_to_target(target_folder, source)

        # generate base folder
        if self.config.get('create_base_folder'):
            name_available = input('Available Name for {}*: '.format(self.app['name']))
            if name_available== '':
                print('Available name is empty. Please try again.')
                sys.exit('Available name is empty. Please try again.')

            self.create_folder(target_folder, self.app['name'], *name_available.split('.'))

        # generate content for dynamic files
        for file_name in self.config.get('files_to_parse'):
            self.parse_file(
                target_folder, self.app['name'], file_name.strip())

        # create static files
        for obj in self.config.get('static_files'):
            instructions = obj.strip().split('>')

            #  get static file content
            self.create_file(
                self.static_handler.get_file(instructions[0]),
                target_folder, self.app['name'], instructions[1])

        # remove files
        for file_name in self.config.get('files_to_delete'):
            self.remove_file(
                target_folder, self.app['name'], file_name.strip())

        return True


lib = Library(pathlib.Path().absolute(), lib_type)
lib.generate(app, target_folder)
