import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Api, Namespace

from logger_config import logger_initial_config


app = Flask(__name__)

app_config = 'config.{}'.format(os.environ.get('APP_SETTINGS', 'Config'))
app.config.from_object(app_config)

app.url_map.strict_slashes = False

logger_initial_config(service_name='ras-frontstage-api', log_level=app.config['LOGGING_LEVEL'])

auth = HTTPBasicAuth()

api = Api(title='Frontstage-API', default='info', default_label=None)

passwords_api = Namespace('passwords', path='/passwords')
register_api = Namespace('register', path='/register')
secure_messaging_api = Namespace('secure-messaging', path='/secure-messaging')
sign_in_api = Namespace('sign-in', path='/sign-in')
surveys_api = Namespace('surveys', path='/surveys')

api.add_namespace(passwords_api)
api.add_namespace(register_api)
api.add_namespace(secure_messaging_api)
api.add_namespace(sign_in_api)
api.add_namespace(surveys_api)


@auth.get_password
def get_pw(username):
    config_username = app.config['SECURITY_USER_NAME']
    config_password = app.config['SECURITY_USER_PASSWORD']
    if username == config_username:
        return config_password


# Import files containing endpoints to bind them to their respective namespaces
import frontstage_api.error_handlers  # NOQA # pylint: disable=wrong-import-position
import frontstage_api.resources.info  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.secure_messaging.get_message import GetMessageView  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.secure_messaging.get_message_list import GetMessagesList  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.secure_messaging.send_message import SendMessage  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.sign_in.sign_in import SignIn  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.passwords.request_password_change import RequestPasswordChange  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.passwords.change_password import ChangePassword  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.passwords.verify_password_token import VerifyPasswordToken  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.register.validate_enrolment import ValidateEnrolment  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.register.confirm_organisation_survey import ConfirmOrganisationSurvey  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.register.create_account import CreateAccount  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.register.verify_email import VerifyEmail  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.register.resend_verification_email import ResendVerificationEmail  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.surveys.get_surveys_list import GetSurveysList  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.surveys.access_case import GetAccessCase  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.surveys.download_collection_instrument import DownloadCollectionInstrument  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.surveys.upload_collection_instrument import UploadCollectionInstrument  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.surveys.add_survey import AddSurvey  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.surveys.confirm_add_organisation_survey import ConfirmAddOrganisationSurvey  # NOQA # pylint: disable=wrong-import-position
from frontstage_api.resources.surveys.generate_eq_url import GenerateEqUrl

api.init_app(app)
