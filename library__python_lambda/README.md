
# testing local
pip install python-lambda-local
python-lambda-local -f lambda_handler lambda_function.py event.json

=> python-lambda-local -f api_app lambda_proxy_app.py lambda_event.json
pre-commit install --hook-type pre-push
