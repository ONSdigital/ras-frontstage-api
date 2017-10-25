import json
import logging
from pathlib import Path

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api, app


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/info')
class Info(Resource):

    @staticmethod
    def get():
        _health_check = {}
        if Path('git_info').exists():
            with open('git_info') as io:
                _health_check = json.loads(io.read())

        info = {
            "name": app.config['NAME'],
            "version": app.config['VERSION'],
        }
        info = dict(_health_check, **info)

        return make_response(jsonify(info), 200)
