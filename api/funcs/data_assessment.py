import json
import os
from typing import Any

import lmql
from dotenv import load_dotenv

from gql_.queries_ import query_get_vacancy
from paths import LOCAL_MODELS_FOLDER
from utils import load_config

config = load_config("models")

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
MODEL_BACKEND = os.getenv("MODEL_BACKEND")
LOCAL_MODEL_TOKENIZER = config["local"]["tokenizer"]

lmql_model = (
    lmql.model(f"llama.cpp:{MODEL_PATH}", endpoint="localhost:9999", tokenizer=LOCAL_MODEL_TOKENIZER)
    if MODEL_BACKEND == "llamacpp"
    else lmql.model(MODEL_PATH, endpoint="localhost:9999")
)


@lmql.query()
def _analyse_resume_bullet_query(bullet, job_data):  # type: ignore[return,empty-body, no-untyped-def]
    # fmt: off
    '''lmql
    sample(1, 0.2)
        "You assume the role of an expert human resources manager, hiring the best talent for the role."
        "You will be given a resume bullet from candidate's resume for assessment."
        "You must compare it against the job responsibilities and requirements and provide an analysis for candidate to improve their resume.\n"
        "Resume bullet: {bullet}\n"
        "Job requirements and responsibilities: {job_data}\n"
        "Is resume bullet relevant to job requirements and responsibilities?:[BOOL_RELEVANCE]"
        "Does resume bullet match job requirements and responsibilities?:[BOOL_MATCH]"
        "Briefly explain the relevancy or match reason of the resume bullet:[STRING_EXPLANATION]"
    from lmql_model
    where
    STOPS_AT(STRING_EXPLANATION, "\n") and len(TOKENS(STRING_EXPLANATION)) < 240
     and BOOL_RELEVANCE in ["true", "false"] and BOOL_MATCH in ["true", "false"]
    '''
    # fmt: on


@lmql.query()
def _create_example_resume_bullet(bullet, job_data):  # type: ignore[return,empty-body, no-untyped-def]
    # fmt: off
    '''lmql
    sample(1, 0.2)
        "You assume the role of an expert human resources manager, hiring the best talent for the role."
        "You will be given a resume bullet from candidate's resume."
        "Create an example bullet point from original, tailored to the job requirements and responsibilities.\n"
        "Resume bullet: {bullet}\n"
        "Job requirements and responsibilities: {job_data}"
        "Example bullet point:•[STRING_EXAMPLE]"
    from lmql_model
    where
        STOPS_AT(STRING_EXAMPLE, ".") and len(TOKENS(STRING_EXAMPLE)) < 150
    '''
    # fmt: on


def analyse_resume_bullet(data: dict[str, Any]) -> list[dict[str, Any]]:  # TODO Schema Validation
    bullet = data["bullet"] if isinstance(data["bullet"], list) else [data["bullet"]]
    job_uid = data["job_uid"]
    job_data = query_get_vacancy(job_uid)
    results = [_analyse_resume_bullet_query(b, json.dumps(job_data)) for b in bullet]
    json_results = []
    for i, result in enumerate(results):
        json_result = {
            "is_match": result.variables["BOOL_MATCH"],
            "is_relevant": result.variables["BOOL_RELEVANCE"],
            "relevance_or_match_reason": result.variables["STRING_EXPLANATION"].strip(),
            "bullet": bullet[i],
        }
        json_results.append(json_result)
    return json_results


def create_example_resume_bullet(data: dict[str, Any]) -> Any:  # TODO Schema Validation
    bullet = data["bullet"]
    job_uid = data["job_uid"]
    job_data = query_get_vacancy(job_uid)

    result = _create_example_resume_bullet(bullet, json.dumps(job_data))
    return result.variables["STRING_EXAMPLE"].strip()
