build:
	pipenv install --dev

lint:
	pipenv run flake8 ./frontstage_api ./tests
	pipenv check ./frontstage_api ./tests

test: lint
	pipenv run python run_tests.py

start:
	pipenv run python run.py
