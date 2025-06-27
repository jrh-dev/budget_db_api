"""
api/__init__.py
This module initialises the FastAPI application and includes the router from the endpoints module.
It sets up logging to a file named "api.log" and configures the FastAPI app.
"""

import logging
from fastapi import FastAPI
import endpoints

logging.basicConfig(filename="api.log", level=logging.INFO)

app = FastAPI()

app.include_router(endpoints.router)