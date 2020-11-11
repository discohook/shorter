class ApiError(Exception):
    status_code = 500
    default_message = "Internal Server Error"

    @property
    def message(self):
        try:
            return self.args[0]
        except IndexError:
            return self.default_message

    @property
    def payload(self):
        try:
            return self.args[1]
        except IndexError:
            return {}


class BadRequestError(ApiError):
    status_code = 400
    default_message = "Bad Request"


class NotFoundError(ApiError):
    status_code = 404
    default_message = "Not Found"
