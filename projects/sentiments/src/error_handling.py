# projects/sentiments/src/error_handling.py
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Union

class ErrorHandling:

    @staticmethod
    async def handle_validation_error(request: Request, exc: Union[RequestValidationError, HTTPException]):
        """
        Handle validation errors for the API by returning a JSON response with an error message and a 400 status code.
        """
        errors = exc.errors() if isinstance(exc, RequestValidationError) else [{"msg": str(exc)}]
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"message": "Validation error", "errors": errors}
        )

    @staticmethod
    async def handle_http_exception(request: Request, exc: HTTPException):
        """
        Handle general HTTP exceptions by returning a JSON response with an error message and the status code from the exception.
        If the exception does not carry a specific message, a generic server error message is used.
        """
        status_code = exc.status_code if exc.status_code else HTTP_500_INTERNAL_SERVER_ERROR
        detail = exc.detail if exc.detail else "An error occurred on the server."
        return JSONResponse(
            status_code=status_code,
            content={"message": detail}
        )

    @staticmethod
    async def handle_generic_exception(request: Request, exc: Exception):
        """
        Handle non-HTTP exceptions that may occur during request processing by returning a JSON response with a generic error message and a 500 status code.
        """
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred on the server."}
        )
