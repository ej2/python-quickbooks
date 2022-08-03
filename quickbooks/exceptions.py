

class QuickbooksException(Exception):
    def __init__(self, message, error_code=0, detail=""):
        super(QuickbooksException, self).__init__(message)

        self.error_code = error_code
        self.detail = detail
        self.message = message
    def __str__(self) -> str:
        return f"QB Exception {self.error_code}: {self.message}\n{self.detail}"
    def __iter__(self):
        yield "error_code", self.error_code
        yield "detail", self.detail
        yield "message", self.message

class AuthorizationException(QuickbooksException):
    """
    Quickbooks Error Codes from 1 to 499
    """
    def __str__(self):
        return f"QB Auth Exception {self.error_code}: {self.message}\n{self.detail}"


class UnsupportedException(QuickbooksException):
    """
    Quickbooks Error Codes from 500 to 599
    """
    def __str__(self):
        return f"QB Unsupported Exception {self.error_code}: {self.message}\n{self.detail}"


class GeneralException(QuickbooksException):
    """
    Quickbooks Error Codes from 600 to 1999
    """
    def __str__(self):
        return f"QB General Exception {self.error_code}: {self.message}\n{self.detail}"


class ValidationException(QuickbooksException):
    """
    Quickbooks Error Codes from 2000 to 4999
    """
    def __str__(self):
        return f"QB Validation Exception {self.error_code}: {self.message}\n{self.detail}"


class SevereException(QuickbooksException):
    """
    Quickbooks Error Codes greater than 10000
    """
    def __str__(self):
        return f"QB Severe Exception {self.error_code}: {self.message}\n{self.detail}"


class ObjectNotFoundException(QuickbooksException):
    """
    Quickbooks Error Code 610
    """
    def __str__(self):
        return f"QB Object Not Found Exception {self.error_code}: {self.message}\n{self.detail}"

