from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest


class RequestBodyError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
