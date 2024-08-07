from typing import Union

from fastapi import HTTPException, status

from app.utils.constants import *


class APIException(Exception):
    def __init__(self, code: str, msg: str):
        super().__init__(msg)
        self.code = code

    def get_code(self) -> str:
        return self.code


class APIExceptionToHTTP:
    def __init__(self):
        self.error_dict = {
            UNKNOWN_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            EXTERNAL_SERVICE_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            FLIGTH_INFO_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
            SEND_CHAT_INFORMATION_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            PLACE_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
            OPENAI_ERROR: status.HTTP_503_SERVICE_UNAVAILABLE,
        }

    def convert(
        self, err: APIException, headers: Union[dict, None] = None
    ) -> HTTPException:
        err_code = err.get_code()
        # Return 500 INTERNAL SERVER ERROR as default status
        err_http_status = self.error_dict.get(
            err_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        err_detail = f"{err_code}: {str(err)}"
        return HTTPException(
            status_code=err_http_status, detail=err_detail, headers=headers
        )
