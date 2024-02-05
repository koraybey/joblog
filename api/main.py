import os
import os.path
from datetime import datetime

from flask import Flask, flash, redirect, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

import uploads
from config import secret
from helpers.data_structuring import (
    generate_candidate_data,
    generate_create_vacancy_data,
    generate_job_posting_data,
)
from helpers.utils import extract_text_from_pdf, scrape_job_posting

UPLOAD_FOLDER = os.path.dirname(uploads.__file__)
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

app = Flask(__name__)
app.secret_key = secret["api"]
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
CORS(app)


@app.route("/createVacancy", methods=["POST"])
def create_vacancy():
    if request.method == "POST":
        data = request.get_json()
        if "html" not in data:
            return {"error": "No HTML content provided."}, 400
        vacancy_data = generate_create_vacancy_data(scrape_job_posting(data))
        # TODO Prepare server deployment first.
        # vacancy_mutation_input = create_vacancy_mutation(vacancy_data)
    return {"success": vacancy_data}, 200


@app.route("/createCandidate", methods=["POST"])
def create_candidate():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
        uploaded_file = upload_file(request.files["file"])
        uploaded_file_str = extract_text_from_pdf(uploaded_file["path"])
        candidate_data = generate_candidate_data(uploaded_file_str)
    return {"success": candidate_data}, 200


@app.route("/createJobPosting", methods=["POST"])
def create_job_posting():
    if request.method == "POST":
        data = request.get_json()
        if "html" not in data:
            return {"error": "No HTML content provided."}, 400
        job_posting_data = generate_job_posting_data(scrape_job_posting(data))
    return {"success": job_posting_data}, 200


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file):
    if file.filename == "":
        flash("No selected file.")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(
            f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}-{file.filename}"
        )
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        return {
            "filename": filename,
            "path": path,
        }


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
