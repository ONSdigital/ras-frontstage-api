# ras-frontstage-api
[![Build Status](https://travis-ci.org/ONSdigital/ras-frontstage-api.svg?branch=master)](https://travis-ci.org/ONSdigital/ras-frontstage-api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/138de7ebc3d246a6bddabec6f9209c8a)](https://www.codacy.com/app/ONSDigital/ras-frontstage-api)
[![codecov](https://codecov.io/gh/ONSdigital/ras-frontstage-api/branch/master/graph/badge.svg)](https://codecov.io/gh/ONSdigital/ras-frontstage-api)

API to handle interfacing between the Frontstage and internal micro-services

## Setup
Created using python 3.6

Create a new virtual environment for python3
```
mkvirtualenv --python=</path/to/python3.6> <your env name>
```

Install dependencies using pip
```
pip install -r requirements.txt
```

Start server
```
python run.py
```

## Run Tests

Install test dependencies using pip
```
pip install -r test-requirements.txt
```

Run tests
```
py.test tests/
```

Run tests with coverage
```
py.test tests/ --cov=frontstage_api
```

## Configuration

Environment variables available for configuration are listed below:

| Environment Variable            | Description                                     | Default
|---------------------------------|-------------------------------------------------|-------------------------------
| NAME                            | Name of application                             | 'ras-frontstage-api'
| VERSION                         | Version number of application                   | '0.0.1' (manually update as application updates)
| APP_SETTINGS                    | Which config to use                             | 'Config' (DevelopmentConfig is set in run.py)
| PORT                            | Which port application runs on                  | '8083'
| LOGGING_LEVEL                   | Level which the application logs at             | 'INFO' ('DEBUG' for DevelopmentConfig)
| MESSAGE_LIMIT                   | Maximum number of messages to return from messaging service | 1000


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