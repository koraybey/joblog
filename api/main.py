import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, request
from flask_cors import CORS
from waitress import serve
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from exceptions_ import UnconfiguredEnvironmentError
from funcs.data_assessment import analyse_resume_bullet, create_example_resume_bullet
from funcs.data_structuring import generate_candidate_data
from gql_.mutations_ import mutation_create_vacancy, mutation_delete_vacancy
from gql_.queries_ import query_get_vacancy
from paths import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from utils import extract_text_from_pdf, scrape_from_linkedin

load_dotenv()

FLASK_API_KEY = os.getenv("FLASK_API_KEY")
API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
ENV = os.getenv("ENV")

app = Flask(__name__)
app.secret_key = FLASK_API_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)


@app.route("/createVacancy", methods=["POST"])
def create_vacancy() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if all(v is not None for v in ["html", "url"]) in data:
            return {"error": "URL and HTML content is not provided."}, 400
        scraped_data = scrape_from_linkedin(data)
        result = mutation_create_vacancy(scraped_data)
    return {"response": result}, 200


@app.route("/getVacancy", methods=["GET"])
def get_vacancy() -> tuple[dict, int]:
    if request.method == "GET":
        data = request.get_json()
        if "uid" not in data:
            return {"error": "uid is not provided."}, 400
        result = query_get_vacancy(data["uid"])
    return {"response": result}, 200


@app.route("/deleteVacancy", methods=["POST"])
def delete_vacancy() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if "uid" not in data:
            return {"error": "uid is not provided."}, 400
        result = mutation_delete_vacancy(data["uid"])
    return {"response": result}, 200


@app.route("/createCandidate", methods=["POST"])
def create_candidate() -> tuple[dict, int]:
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
        uploaded_file = upload_file(request.files["file"])
        uploaded_file_str = extract_text_from_pdf(uploaded_file)
        result = generate_candidate_data(uploaded_file_str)
    return {"response": result}, 200


@app.route("/createAnalysis", methods=["POST"])
def create_analysis() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if all(v is not None for v in ["bullet", "job_uid"]) in data:
            return {"error": "Resume bullet or job_uid not provided."}, 400
        result = analyse_resume_bullet(data)
    return {"response": result}, 200


@app.route("/createExample", methods=["POST"])
def create_example() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if any(v is None for v in ["bullet", "job_uid"]) in data:
            return {"error": "Resume bullet or job_uid not provided."}, 400
        result = create_example_resume_bullet(data)
    return result, 200


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file: FileStorage) -> Path:
    if file.filename == "":
        flash("No selected file.", "error")
    if file.filename is not None and allowed_file(file.filename):
        filename = secure_filename(f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}-{file.filename}")
        path = Path(app.config["UPLOAD_FOLDER"] / filename)
        file.save(path)
    return path


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
