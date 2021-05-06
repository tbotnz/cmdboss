

class CMDBOSSException(Exception):
    """Base CMDBOSS Exception"""


class CMDBOSSFileExists(CMDBOSSException):
    """File Mgr File Already Exists"""


class CMDBOSSHTTPException(Exception):
    """HTTP Exception Handler"""
    def __init__(self, status_code: int, result: list):
        self.status_code = status_code
        self.status = "error"
        self.result = result


class CMDBOSSCallbackHTTPException(Exception):
    """Callback HTTP Exception Handler"""
