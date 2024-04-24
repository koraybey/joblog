import logging
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from waitress import serve

from exceptions import UnconfiguredEnvironmentError
from mutations import create_vacancy as m_create_vacancy
from mutations import delete_vacancy as m_delete_vacancy
from queries import get_vacancy as q_get_vacancy
from utils import scrape_from_linkedin

load_dotenv()

FLASK_API_KEY = os.getenv("FLASK_API_KEY")
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
ENV = os.getenv("ENV")

app = Flask(__name__)
app.secret_key = FLASK_API_KEY
CORS(app)


@app.route("/createVacancy", methods=["POST"])
def create_vacancy() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if all(v is not None for v in ["html", "url"]) in data:
            return {"error": "URL and HTML content is not provided."}, 400
        scraped_data = scrape_from_linkedin(data)
        result = m_create_vacancy(scraped_data)
    return {"response": result}, 200


@app.route("/getVacancy", methods=["GET"])
def get_vacancy() -> tuple[dict, int]:
    if request.method == "GET":
        data = request.get_json()
        if "uid" not in data:
            return {"error": "uid is not provided."}, 400
        result = q_get_vacancy(data["uid"])
    return {"response": result}, 200


@app.route("/deleteVacancy", methods=["POST"])
def delete_vacancy() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if "uid" not in data:
            return {"error": "uid is not provided."}, 400
        result = m_delete_vacancy(data["uid"])
    return {"response": result}, 200


if __name__ == "__main__":
    if any(v is None for v in [API_HOST, API_PORT, FLASK_API_KEY]):
        raise UnconfiguredEnvironmentError
    if ENV is None or ENV == "dev":
        app.run(
            debug=True,  # noqa: S201
            port=(int(API_PORT) if API_PORT is not None else None),
            host=API_HOST,
        )
    else:
        logger = logging.getLogger("waitress")
        logger.setLevel(logging.INFO)
        serve(app, port=API_PORT, host=API_HOST)
