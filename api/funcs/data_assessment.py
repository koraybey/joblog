import json
from typing import Any

import lmql

from gql_.queries_ import query_get_vacancy
from paths import LOCAL_MODELS_FOLDER
from utils import load_config

config = load_config("models")

BACKEND = config["server"]["backend"]
MODEL = config["server"]["model"]
HOST = config["server"]["host"]
PORT = config["server"]["port"]
REPO_ID = config["server"]["repo_id"]
TOKENIZER = config["server"]["tokenizer"]

lmql_model = (
    lmql.model(f"llama.cpp:{LOCAL_MODELS_FOLDER.absolute()}/{MODEL}", endpoint=f"{HOST}:{PORT}", tokenizer=TOKENIZER)
    if BACKEND == "llamacpp"
    else lmql.model(REPO_ID, endpoint=f"{HOST}:{PORT}")
)


@lmql.query(model=lmql_model, verbose=True)
def _analyse_resume_bullet_query(bullet, job_data):  # type: ignore[return,empty-body, no-untyped-def]
    # fmt: off
    '''lmql
    sample(n=1, temperature=0.5, max_len=2048)
        "{:system}"
        "You assume the role of an expert human resources manager, hiring the best talent for the role."
        "You will be given a resume bullet from candidate's resume for assessment."
        "You must compare it against the job responsibilities and requirements and provide an analysis for candidate to improve their resume."
        "{:user}Resume bullet:\n{bullet}\n"
        "{:user}Job description:\n{job_data}\n"
        "{:user}Is resume bullet relevant to job description?"
        "{:assistant}[BOOL_RELEVANCE]"
        "{:user}Does resume bullet match job description?"
        "{:assistant}[BOOL_MATCH]"
        "{:user}Explain the relevancy or match reason in a few sentences. You must always provide a reason even if there is no match and relevance."
        "{:assistant}[STRING_EXPLANATION]"
        "{:user}Provide a more relevant, better aligned resume bullet example."
        "{:assistant}[STRING_EXAMPLE]"
    where
    STOPS_AT(STRING_EXPLANATION, "\n") and len(TOKENS(STRING_EXPLANATION)) < 200 and STOPS_AT(STRING_EXAMPLE, "\n") and len(TOKENS(STRING_EXAMPLE)) < 200
     and BOOL_RELEVANCE in ["true", "false"] and BOOL_MATCH in ["true", "false"]
    '''
    # fmt: on


@lmql.query(model=lmql_model, verbose=True)
def _create_example_resume_bullet(bullet, job_data):  # type: ignore[return,empty-body, no-untyped-def]
    # fmt: off
    '''lmql
    sample(n=1, temperature=0.5, max_len=2048)
        "{:system}"
        "You are an expert human resources manager."
        "You will be given a resume bullet from candidate's resume for assessment."
        "Find the most relevant details from the job description and improve the resume bullet point to align it better with the relevant requirements and responsibilities."
        "{:user}Resume bullet:\n{bullet}\n"
        "{:user}Job description:\n{job_data}\n"
        "{:user}Improved bullet point:"
        "{:assistant}[EXAMPLE]"
        "{:user}Reason for improvement:"
        "{:assistant}[REASON]"
    where
        len(TOKENS(REASON)) < 200 and len(TOKENS(EXAMPLE)) < 200
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
            "match": result.variables["BOOL_MATCH"],
            "relevance": result.variables["BOOL_RELEVANCE"],
            "reason": result.variables["STRING_EXPLANATION"].strip(),
            "example": result.variables["STRING_EXAMPLE"].strip(),
            "bullet": bullet[i],
        }
        json_results.append(json_result)
    return json_results


def create_example_resume_bullet(data: dict[str, Any]) -> Any:  # TODO Schema Validation
    bullet = data["bullet"]
    job_uid = data["job_uid"]
    job_data = query_get_vacancy(job_uid)

    result = _create_example_resume_bullet(bullet, json.dumps(job_data))
    json_result = {
        "example": result.variables["EXAMPLE"].strip(),
        "reason": result.variables["REASON"].strip(),
    }
    return json_result
