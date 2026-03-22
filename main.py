from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
import uvicorn
import logging
from logging.config import dictConfig
import os
from routes import user, product, order
from auth import verify_token

# Define logging configuration
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})

# Create the FastAPI application instance
def create_app() -> FastAPI:
    app = FastAPI(
        title="E-commerce Store",
        description="E-commerce store with user authentication, products, and order management",
        version="1.0.0"
    )

    # Define CORS configuration
    origins = [
        "http://localhost:3000",
        "https://example.com"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Define authentication middleware
    async def get_token(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ):
        try:
            return verify_token(token.credentials)
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    # Include routes
    app.include_router(user.router, prefix="/users", dependencies=[Depends(get_token)])
    app.include_router(product.router, prefix="/products", dependencies=[Depends(get_token)])
    app.include_router(order.router, prefix="/orders", dependencies=[Depends(get_token)])

    # Define error handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError
    ):
        error_messages = []
        for error in exc.errors():
            error_messages.append({
                "location": error["loc"],
                "message": error["msg"],
                "type": error["type"]
            })
        return JSONResponse(
            status_code=422,
            content={"errors": error_messages}
        )

    return app

# Define main function to run the application
def main():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

if __name__ == "__main__":
    main()