# coding=utf-8
class TextocatApiException(Exception):
    def __init__(self, message, http_code):
        super(TextocatApiException, self).__init__(message)
        self.http_code = http_code


class WrongFormatException(TextocatApiException):
    def __init__(self):
        super(WrongFormatException, self).__init__('Wrong format.', 400)


class UnauthorizedException(TextocatApiException):
    def __init__(self):
        super(UnauthorizedException, self).__init__('User is not authorized. Pass correct auth token.', 401)


class MonthlyDataLimitException(TextocatApiException):
    def __init__(self):
        super(MonthlyDataLimitException, self).__init__('Monthly limit of processed data exhausted.', 402)


class PermissionException(TextocatApiException):
    def __init__(self):
        super(PermissionException, self).__init__('User don\'t have enough permissions.', 403)


class CollectionNotFountException(TextocatApiException):
    def __init__(self):
        super(CollectionNotFountException, self).__init__('Collection not found.', 404)


class UnsupportedMethodException(TextocatApiException):
    def __init__(self):
        super(UnsupportedMethodException, self).__init__('Unsupported method for this type of operation.', 405)


class UnsupportedInputException(TextocatApiException):
    def __init__(self):
        super(UnsupportedInputException, self).__init__('Unsupported input', 406)


class CollectionInProcessException(TextocatApiException):
    def __init__(self):
        super(CollectionInProcessException, self).__init__('Collection in progress.', 406)


class InputDataLimitException(TextocatApiException):
    def __init__(self):
        super(InputDataLimitException, self).__init__('Input data limit exceeded', 413)


class UnsupportedMimeTypeException(TextocatApiException):
    def __init__(self):
        super(UnsupportedMimeTypeException, self).__init__('This MIME type is not supported.', 415)


class RequestsLimitException(TextocatApiException):
    def __init__(self):
        super(RequestsLimitException, self).__init__('Requests limit exceeded.', 416)


class ConcurrentConnectionsLimitException(TextocatApiException):
    def __init__(self):
        super(ConcurrentConnectionsLimitException, self).__init__(
            'You have exceeded the number of concurrent connections.', 429)


class ServiceUnavailable(TextocatApiException):
    def __init__(self):
        super(ServiceUnavailable, self).__init__('Service unavailable.', 503)


class InternalErrorException(TextocatApiException):
    def __init__(self):
        super(InternalErrorException, self).__init__('Internal error.', 500)


class UnexpectedHttpCodeException(Exception):
    def __init__(self, http_code):
        super(UnexpectedHttpCodeException, self).__init__(str.format('Unexpected http code {0}', http_code))


def raise_by_http_code(http_code):
    excepts = {
        400: WrongFormatException,
        401: UnauthorizedException,
        402: MonthlyDataLimitException,
        403: PermissionException,
        404: CollectionNotFountException,
        405: UnsupportedMethodException,
        406: UnsupportedInputException,
        413: InputDataLimitException,
        415: UnsupportedMimeTypeException,
        416: RequestsLimitException,
        429: ConcurrentConnectionsLimitException,
        500: InternalErrorException,
        503: ServiceUnavailable,
    }

    if http_code in excepts:
        raise excepts[http_code]()

    raise UnexpectedHttpCodeException(http_code)