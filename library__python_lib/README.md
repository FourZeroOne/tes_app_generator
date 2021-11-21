# {{ app.name }}

## install dev
virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt -r requirements_dev.txt
pre-commit install --hook-type pre-push

## build and deploy
python setup.py sdist bdist_wheel
s3pypi --bucket pypi.fourzero.one
