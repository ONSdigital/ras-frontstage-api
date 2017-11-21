# ras-frontstage-api
[![Build Status](https://travis-ci.org/ONSdigital/ras-frontstage-api.svg?branch=master)](https://travis-ci.org/ONSdigital/ras-frontstage-api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/138de7ebc3d246a6bddabec6f9209c8a)](https://www.codacy.com/app/ONSDigital/ras-frontstage-api)
[![codecov](https://codecov.io/gh/ONSdigital/ras-frontstage-api/branch/master/graph/badge.svg)](https://codecov.io/gh/ONSdigital/ras-frontstage-api)

API to handle interfacing between the Frontstage and internal micro-services

## Setup
Created using python 3.6

Install dependencies using [pipenv](https://docs.pipenv.org/index.html)
```
pip install -U pipenv
pipenv install
```

Start server
```
pipenv run python run.py
```

## Run Tests

Install test dependencies using pipenv
```
pipenv install --dev
```

Run tests with coverage
```
pipenv run python run_tests.py
```

Run flake8 check
```
pipenv check --style .
```

## Swagger
A swagger UI definition of the API is automatically generated using Flask-RESTPlus and can be found at the root of the application, by default [localhost:8083]('http://localhost:8083')

## Configuration

Environment variables available for configuration are listed below:
Defaults in brackets are only set when APP_SETTINGS is set to DevelopmentConfig, this is done automatically when using run.py script to start

| Environment Variable            | Description                                     | Default
|---------------------------------|-------------------------------------------------|-------------------------------
| NAME                            | Name of application                             | 'ras-frontstage-api'
| VERSION                         | Version number of application                   | '0.0.1'
| APP_SETTINGS                    | Which config to use                             | 'Config'
| PORT                            | Which port application runs on                  | '8083'
| LOGGING_LEVEL                   | Level which the application logs at             | 'INFO' ('DEBUG')
| MESSAGE_LIMIT                   | Maximum number of messages to return from messaging service | 1000
| SECURITY_USER_NAME              | Username for basic auth                         | None ('test_user')
| SECURITY_USER_PASSWORD          | Password for basic auth                         | None ('test_password')
| DJANGO_CLIENT_ID                | Username for authroisation to django server     | None ('test@test.test')
| DJANGO_CLIENT_SECRET            | Password for authroisation to django server     | None ('testtest')

For each external application which frontstage-api communicates with there are 3 environment variables e.g. for the RAS Secure Messaging service:

| Environment Variable                | Description                              | Default
|-------------------------------------|------------------------------------------|-------------------------------
| RAS_SECURE_MESSAGE_SERVICE_HOST     | Host address for secure message service  | 'localhost'
| RAS_SECURE_MESSAGE_SERVICE_PORT     | Port for secure message service          | '5050'
| RAS_SECURE_MESSAGE_SERVICE_PROTOCOL | Protocol used for secure message service | 'http'

The services these variables exist for are listed below with the beginnings of their variables and their github links:

| Service                         | Start of variables          | Github
|---------------------------------|-----------------------------|-----------------------------
| Secure message service          | RAS_SECURE_MESSAGE_SERVICE  | https://github.com/ONSdigital/ras-secure-message
| Case service                    | RM_CASE_SERVICE             | https://github.com/ONSdigital/rm-case-service
| IAC service                     | RM_IAC_SERVICE              | https://github.com/ONSdigital/iac-service
| Collection exercise service     | RM_COLLECTION_EXERCISE_SERVICE      | https://github.com/ONSdigital/rm-collection-exercise-service
| Survey service                  | RM_SURVEY_SERVICE           | https://github.com/ONSdigital/rm-survey-service
| Party service                   | RAS_PARTY_SERVICE           | https://github.com/ONSdigital/ras-party
| Oauth2 service                  | RAS_OAUTH_SERVICE           | https://github.com/ONSdigital/django-oauth2-test
| Collection instrument service   | RAS_COLLECTION_INSTRUMENT_SERVICE | https://github.com/ONSdigital/ras-collection-instrument
