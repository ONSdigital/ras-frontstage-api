class FailedRequest(Exception):

    def __init__(self, method, url, exception=None):
        super().__init__()
        self.method = str(method)
        self.url = url
        self.exception = str(exception) if exception else None


class InvalidRequestMethod(Exception):

    def __init__(self, method, url):
        super().__init__()
        self.method = str(method)
        self.url = url


class NoJWTError(Exception):
    pass


class UnexpectedStatusCode(Exception):

    def __init__(self, method, url, status_code, content):
        super().__init__()
        self.method = method
        self.url = url
        self.status_code = status_code
        self.content = str(content)