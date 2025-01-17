import logging
import os
from typing import Any, Callable, Optional, Tuple, TypedDict, Union

from dotenv import load_dotenv
from flask import Flask, Response, request
from flask_cors import CORS
from waitress import serve

from exceptions import UnconfiguredEnvironmentError
from gql_operations.mutations import create_vacancy as m_create_vacancy
from gql_operations.mutations import delete_vacancy as m_delete_vacancy
from gql_operations.queries import get_vacancy as q_get_vacancy
from utils import scrape_from_linkedin

load_dotenv()

FLASK_API_KEY = os.getenv("FLASK_API_KEY")
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
ENV = os.getenv("ENV")

app = Flask(__name__)
if FLASK_API_KEY is not None:
    app.secret_key = FLASK_API_KEY

# Type definitions
ResponseType = Tuple[dict[str, Any], int]
RequestData = TypedDict('RequestData', {'html': str, 'url': str}, total=False)

def add_cors_headers(response: Response) -> Response:
    """Add CORS headers to the response."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }
    for key, value in headers.items():
        response.headers[key] = value
    return response

def handle_request_error(message: str, status_code: int = 400) -> ResponseType:
    """Handle request errors with consistent format."""
    return {"error": message}, status_code

def validate_request_data(data: dict[str, Any], required_fields: list[str]) -> Optional[ResponseType]:
    """Validate request data for required fields."""
    if not all(field in data for field in required_fields):
        return handle_request_error(f"Required fields missing: {', '.join(required_fields)}")
    return None

# Simple CORS configuration
CORS(app, 
     origins=["*"],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

@app.before_request
def handle_preflight() -> Optional[Response]:
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        return add_cors_headers(response)
    return None

@app.after_request
def after_request(response: Response) -> Response:
    return add_cors_headers(response)

def create_route_handler(handler_func: Callable[[dict[str, Any]], Any], required_fields: list[str]) -> Callable[[], ResponseType]:
    """Create a route handler with common error handling and validation."""
    def wrapper() -> ResponseType:
        if request.method == "OPTIONS":
            return {"success": True}, 200
            
        if request.method not in ["GET", "POST"]:
            return handle_request_error("Method not allowed", 405)
            
        data = request.get_json()
        validation_error = validate_request_data(data, required_fields)
        if validation_error:
            return validation_error
            
        try:
            result = handler_func(data)
            return {"response": result}, 200
        except Exception as e:
            return handle_request_error(str(e), 500)
            
    return wrapper

@app.route("/createVacancy", methods=["POST", "OPTIONS"])
def create_vacancy() -> ResponseType:
    return create_route_handler(
        lambda data: m_create_vacancy(scrape_from_linkedin(data)),
        ["html", "url"]
    )()

@app.route("/getVacancy", methods=["GET"])
def get_vacancy() -> ResponseType:
    return create_route_handler(
        lambda data: q_get_vacancy(data["uid"]),
        ["uid"]
    )()

@app.route("/deleteVacancy", methods=["POST"])
def delete_vacancy() -> ResponseType:
    return create_route_handler(
        lambda data: m_delete_vacancy(data["uid"]),
        ["uid"]
    )()

def run_server(host: str, port: Union[str, int]) -> None:
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    serve(app, host=host, port=int(port))

if __name__ == "__main__":
    if any(v is None for v in [API_HOST, API_PORT, FLASK_API_KEY]):
        raise UnconfiguredEnvironmentError
    assert API_HOST is not None
    assert API_PORT is not None
    run_server(API_HOST, API_PORT)