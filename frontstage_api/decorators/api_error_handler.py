from frontstage_api.exceptions.exceptions import ApiError


def api_error_handler(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ApiError as e:
            error_json = {
                "error": {
                    "code": e.error_code,
                    "data": e.data
                }
            }
            return error_json
    return wrapper
