from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

long_description = ''
if path.isfile('README.md'):
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

requirements = []
if path.isfile('requirements.txt'):
    with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        requirements = [line.strip() for line in f]

setup(
    name='{{ app.name }}',
    version='0.1.0',
    description='{{ app.short_description }}',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='{{ app.keywords }}',
    author='{{ app.author }}',
    author_email='{{ app.author_email }}',
    license='{{ app.license_type }}',
    url='{{ app.url }}',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements,
    python_requires='>=3.9'
)
