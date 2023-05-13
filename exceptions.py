class UnauthorizedError(Exception):
    def __init__(self, message="Not authorized"):
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message="Not found"):
        super().__init__(message)


class InternalServerError(Exception):
    def __init__(self, message="Internal server error"):
        super().__init__(message)
