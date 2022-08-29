from requests.exceptions import RequestException


class EndPointServerError(RequestException):
    'Something wrong with end-pont server. Message is not delivered.'
