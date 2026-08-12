from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


def error_response(status: int, code: str, message: str, details: dict | None = None) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message, "details": details or {}})

def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_error(_: Request, exc: HTTPException):
        detail = exc.detail if isinstance(exc.detail, dict) else {"code": "http_error", "message": str(exc.detail), "details": {}}
        return JSONResponse(status_code=exc.status_code, content={"error": detail}, headers=exc.headers)

    @app.exception_handler(Exception)
    async def unhandled(_: Request, __: Exception):
        return JSONResponse(status_code=500, content={"error": {"code": "internal_error", "message": "An unexpected error occurred.", "details": {}}})
