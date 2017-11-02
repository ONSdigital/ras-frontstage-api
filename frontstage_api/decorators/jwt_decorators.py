from functools import wraps
import logging

from structlog import wrap_logger

from frontstage_api.exceptions.exceptions import NoJWTError


logger = wrap_logger(logging.getLogger(__name__))


def get_jwt(request):
    def extract_session(original_function):
        @wraps(original_function)
        def extract_session_wrapper(*args, **kwargs):
            encoded_jwt_token = request.headers.get('jwt')
            if encoded_jwt_token:
                return original_function(encoded_jwt_token, *args, **kwargs)
            else:
                raise NoJWTError
        return extract_session_wrapper
    return extract_session
