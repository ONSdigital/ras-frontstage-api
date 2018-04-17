class ApiError(Exception):

    def __init__(self, url, status_code=None, data=None, description=None, **kwargs):
        super().__init__()
        self.url = url
        self.status_code = status_code
        self.data = data
        self.description = description if description else 'Error during api call'
        self.kwargs = kwargs


class InvalidCaseCategory(Exception):

    def __init__(self, category):
        super().__init__()
        self.category = category


class InvalidSurveyList(Exception):

    def __init__(self, survey_list):
        super().__init__()
        self.survey_list = survey_list


class InvalidRequestMethod(Exception):

    def __init__(self, method, url):
        super().__init__()
        self.method = str(method)
        self.url = url


class NoSurveyPermission(Exception):

    def __init__(self, party_id, case_id, case_party_id):
        super().__init__()
        self.party_id = party_id
        self.case_id = case_id
        self.case_party_id = case_party_id


class NoJWTError(Exception):
    pass


class FileTooLarge(Exception):
    def __init__(self, case_id, party_id, file_size):
        super().__init__()
        self.case_id = case_id
        self.party_id = party_id
        self.file_size = file_size


class InvalidEqPayLoad(Exception):
    def __init__(self, error):
        super().__init__()
        self.error = error
