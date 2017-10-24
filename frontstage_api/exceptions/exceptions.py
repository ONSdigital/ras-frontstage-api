class ApiError(Exception):

    def __init__(self, error_code, data=None):
        super().__init__()
        self.error_code = error_code
        self.data = data


class InvalidRequestMethod(Exception):

    def __init__(self, method, url):
        super().__init__()
        self.method = str(method)
        self.url = url


class NoJWTError(Exception):
    pass
