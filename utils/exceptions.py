class APIException(Exception):
    """Base exception untuk semua error API."""
    status_code = 400
    message = "Terjadi kesalahan"

    def __init__(self, message=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

class NotFoundException(APIException):
    status_code = 404
    message = "Data tidak ditemukan"

class ValidationException(APIException):
    status_code = 400
    message = "data tidak valid"

class ForbiddenException(APIException):
    status_code = 403
    message = "Akses ditolak"