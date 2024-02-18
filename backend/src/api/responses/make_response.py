from fastapi.responses import JSONResponse

def make_response(status, data, message, code = 200) -> JSONResponse:
    content = {
        'status': status,
        'data': data,
        'message': message
    }
    return JSONResponse(
        content=content,
        status_code=code,
    )