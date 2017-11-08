class ApiError(Exception):

    def __init__(self, url, status_code=None, data=None):
        super().__init__()
        self.url = url
        self.status_code = status_code
        self.data = data


class InvalidCaseCategory(Exception):

    def __init__(self, category):
        super().__init__()
        self.category = category


class InvalidRequestMethod(Exception):

    def __init__(self, method, url):
        super().__init__()
        self.method = str(method)
        self.url = url


class NoJWTError(Exception):
    pass
