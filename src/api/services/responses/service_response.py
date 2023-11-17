


class ServiceResponse:
    def __init__(self, response_status: str,data, message: str, http_code: int) -> None:
        self.data = data
        self.response_status = response_status
        self.message = message
        self.http_code = http_code

    