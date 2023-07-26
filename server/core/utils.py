from fastapi.responses import JSONResponse
from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code, detail=detail)


class CustomJSONResponse(JSONResponse):
    def __init__(self, code, message, data, **kwargs):
        response = {'code': code, 'message': message, 'data': data}
        super().__init__(content=response, **kwargs)
