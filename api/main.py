import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, request
from flask_cors import CORS
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from funcs.data_assessment import analyse_resume_bullet, create_example_resume_bullet
from funcs.data_structuring import generate_candidate_data, generate_create_vacancy_data
from gql_.mutations_ import create_vacancy_mutation
from paths import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from utils import check_mps_backend, extract_text_from_pdf, scrape_job_posting

load_dotenv()

FLASK_API_KEY = os.getenv("FLASK_API_KEY")

app = Flask(__name__)
app.secret_key = FLASK_API_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)

check_mps_backend()


@app.route("/createVacancy", methods=["POST"])
def create_vacancy() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if "html" not in data:
            return {"error": "No HTML content provided."}, 400
        scraped_data = generate_create_vacancy_data(scrape_job_posting(data))
        # TODO Prepare server deployment first.
        result = create_vacancy_mutation(scraped_data)
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


@app.route("/assessResumeBullet", methods=["POST"])
def assess_resume_bullet() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if "data" not in data:
            return {"error": "No resume bullet provided."}, 400
        result = analyse_resume_bullet(data["data"])
    return {"response": result}, 200


@app.route("/createExampleResumeBullet", methods=["POST"])
def provide_example_resume_bullet() -> tuple[dict, int]:
    if request.method == "POST":
        data = request.get_json()
        if "data" not in data:
            return {"error": "No resume bullet provided."}, 400
        result = create_example_resume_bullet(data["data"])
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
    app.run(port=5000, host="127.0.0.1")
