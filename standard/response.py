class MessageCode:
    pass


class ErrorMessage:
    pass


def get_error_response(error_code: str, errors: dict):
    return {"code": error_code, "errors": errors}
