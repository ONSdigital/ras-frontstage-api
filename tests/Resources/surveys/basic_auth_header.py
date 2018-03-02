import base64
from frontstage_api import app


def basic_auth_header():
    return {
        'Authorization': 'Basic {}'.format(base64.b64encode(
            bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']),
                  'ascii')).decode("ascii"))
    }
