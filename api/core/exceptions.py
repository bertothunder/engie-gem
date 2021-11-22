import json
import logging
import traceback
from fastapi.requests import Request
from fastapi.responses import JSONResponse


# Error codes
UNEXPECTED = "unexpected_error"
BAD_REQUEST = "bad_request"
BAD_CREDENTIALS = "bad_credentials"
BAD_TOKEN = "bad_token"
UNAUTHORIZED = "unauthorized"
NOT_ALLOWED = "No_permissions_enough"
NOT_FOUND = "not_found"
NO_CONTENT = "no_content"
NOT_IMPLEMENTED = "not_implemented"
IM_A_TEAPOT = "Teapot"


ERRORS = {
    UNEXPECTED: "Enexpected server error occurred.",
    BAD_REQUEST: "Something was wrong with the request payload.",
    UNAUTHORIZED: "Permission denied accessing the resource.",
    NOT_ALLOWED: "No permissions given to execute the given action",
    BAD_TOKEN: "Invalid login token.",
    BAD_CREDENTIALS: "Invalid username/password credentials provided.",
    NOT_FOUND: "Requested resource could not be found.",
    NO_CONTENT: "Found no valid data to return.",
    NOT_IMPLEMENTED: "This feature has not yet been implemented.",
    IM_A_TEAPOT: "I'm a teapot",
}


logger = logging.getLogger("api.core.exceptions")


class APIException(Exception):
    """
    Base exception for webservice API calls
    """

    def __init__(self, msg=None, status_code=500, error_code=UNEXPECTED, response_type="error"):
        super().__init__(self)
        if not msg:
            if error_code not in ERRORS:
                error_code = UNEXPECTED
            msg = ERRORS[error_code]
        self.message = msg
        self.status_code = status_code
        self.error_code = error_code
        self.response_type = response_type

    @property
    def traceback(self):
        """
        Returns a formatted excpt traceback
        :return:
        """
        return traceback.format_exc()

    @property
    def data(self):
        """
        Returns a dict'd representation of the exception data
        :return:
        """
        return {
            "responseType": self.response_type,
            "code": self.error_code,
            "message": self.message,
        }

    def create_response(self, response):
        """
        Returns a response object from exception' data
        :param response:
        :return:
        """
        response.status_code = self.status_code
        response.mimetype = "application/json"
        response.set_data(json.dumps(self.data))
        return response

    def __str__(self):
        """
        Returns the string representation of each API Exception child class
        :return:
        """
        return f"{self.__class__}: {self.message}"


class BadRequestException(APIException):
    """Abstracts Bad request (HTTP 400) in a general case"""

    def __init__(self, msg=None, status_code=400, error_code=BAD_REQUEST):
        super().__init__(msg, status_code, error_code)


class BadTokenException(APIException):
    """Abstracts Unauthorized request (HTTP 401) for an invalid token"""

    def __init__(self, msg=None, status_code=401, error_code=BAD_TOKEN):
        super().__init__(msg, status_code, error_code)


class BadCredentialsException(APIException):
    """Abstracts Unauthorized request (HTTP 401) for invalid credentials"""

    def __init__(self, msg=None, status_code=401, error_code=BAD_CREDENTIALS):
        super().__init__(msg, status_code, error_code)


class UnauthorizedException(APIException):
    """Abstracts the Unauthorized request (HTTP 401) for a general case"""

    def __init__(self, msg=None, status_code=401, error_code=UNAUTHORIZED):
        super().__init__(msg, status_code, error_code)


class NotAllowedException(APIException):
    """ "Abstracts the internal error due to entity not having enough permissions"""

    def __init__(self, msg=None, status_code=403, error_code=NOT_ALLOWED):
        super().__init__(msg, status_code, error_code)


class NotFoundException(APIException):
    """Abstrae Not Found (HTTP 404)"""

    def __init__(self, msg=None, status_code=404, error_code=NOT_FOUND):
        super().__init__(msg, status_code, error_code)


class NoContentException(APIException):
    """
    Abstracts a No Content Response.
    This is not actually an error response (HTTP 204)
    """

    def __init__(self, msg=None, status_code=204, error_code=NO_CONTENT):
        super().__init__(msg, status_code=status_code, error_code=error_code, response_type="warning")


class NotImplementedServiceError(APIException):
    """
    Server seems not to be ready to handle the request, either valid or not (HTTP 501)
    """

    def __init__(self, msg=None, status_code=501, error_code=NOT_IMPLEMENTED):
        super().__init__(msg, status_code, error_code)


class ImATeapotError(APIException):
    """
    This is actually used to distract some weird clients that could be
    attacking or performing wary things on our server (HTTP 418)
    """

    def __init__(self, msg=None, status_code=418, error_code=IM_A_TEAPOT):
        super().__init__(msg, status_code, error_code)


def error_factory(error_code, message=None):
    """
    Return the right exception for the given error code
    :param error_code:
    :param message:
    :return:
    """
    exception_classes = {
        UNEXPECTED: APIException,
        BAD_REQUEST: BadRequestException,
        UNAUTHORIZED: UnauthorizedException,
        NOT_FOUND: NotFoundException,
        NO_CONTENT: NoContentException,
        NOT_IMPLEMENTED: NotImplementedServiceError,
        IM_A_TEAPOT: ImATeapotError,
    }
    if error_code not in ERRORS:
        error_code = UNEXPECTED
    return exception_classes[error_code](message=message, error_code=error_code)


def api_exception_handler(request: Request, error: APIException):
    """
    Give a response when there is an exception when processing the request
    :param request: Request received
    :param error: Exception
    :return:
    """
    logger.error(
        f'Handling "{error.message}" error for [<{request.method}> {request.url}] with headers ["{request.headers}"]'
    )
    item = {
        "message": error.message,
        "code": error.error_code,
        "responseType": error.response_type,
    }

    return JSONResponse(status_code=error.status_code, content=item, media_type="application/json")
