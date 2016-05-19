

class QuickbooksException(Exception):
    def __init__(self, message, error_code=0, detail=""):
        super(QuickbooksException, self).__init__(message)

        self.error_code = error_code
        self.detail = detail
        self.message = message


class AuthorizationException(QuickbooksException):
    """
    Quickbooks Error Codes from 1 to 499
    """
    def __str__(self):
        return "QB Auth Exception: " + self.message + " \n\n" + self.detail


class UnsupportedException(QuickbooksException):
    """
    Quickbooks Error Codes from 500 to 599
    """
    pass


class GeneralException(QuickbooksException):
    """
    Quickbooks Error Codes from 600 to 1999
    """
    pass


class ValidationException(QuickbooksException):
    """
    Quickbooks Error Codes from 2000 to 4999
    """
    pass


class SevereException(QuickbooksException):
    """
    Quickbooks Error Codes greater than 10000
    """
    pass
