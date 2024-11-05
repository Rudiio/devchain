from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import aiofiles

from api_routes import router as api_router
from error_handling import ErrorHandling

# Create an instance of the FastAPI class
app = FastAPI()

# Mount static files, accessible from the '/static' path
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the API routes from api_routes.py
app.include_router(api_router)

# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return await ErrorHandling.handle_http_exception(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await ErrorHandling.handle_validation_error(request, exc)

# Serve index.html for the root path
@app.get("/", response_class=HTMLResponse)
async def read_root():
    async with aiofiles.open('static/index.html', 'r') as file:
        html_content = await file.read()
    return HTMLResponse(content=html_content, status_code=200)

# Entry point to launch the FastAPI server
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
