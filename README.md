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