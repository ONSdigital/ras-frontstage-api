import base64
from frontstage_api import app


def basic_auth_header():
    auth_string = base64.b64encode(
        bytes(f"{app.config['SECURITY_USER_NAME']}:{app.config['SECURITY_USER_PASSWORD']}", 'ascii')
    ).decode("ascii")
    return {
        'Authorization': f'Basic {auth_string}',
    }
