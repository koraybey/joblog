import json

from huggingface_hub import hf_hub_download
from llama_cpp import Llama, LlamaGrammar

from config import config
from helpers.utils import json_schema_to_grammar, json_schema_with_inlining
from models import Candidate, CreateVacancy, JobPosting


def generate_job_posting_data(text: str):
    model_path = hf_hub_download(
        repo_id=config["local"]["repo_id"],
        filename=config["local"]["model"],
    )

    llm = Llama(
        model_path=model_path,
        n_ctx=config["local"]["n_ctx"],
        n_gpu_layers=-1,
        offload_kqv=True,
        verbose=True,
        n_threads=2,
    )
    question = f"""\
    You assume the role of an expert human resources manager. You are tasked to extract job requirements, responsibilities, and skills required from a job posting. Avoid summarization and provide unchanged facts from the job posting.\n
    Your response should contain four sections: Summary, Skills, Requirements and Responsibilities.
    Here is the job posting:\n
    {text}
    """

    output = llm(
        question,
        grammar=LlamaGrammar.from_string(
            json_schema_to_grammar(json_schema_with_inlining(JobPosting), "")
        ),
        max_tokens=config["local"]["max_tokens"],
        temperature=config["local"]["temperature"],
    )

    print(json.dumps(json.loads(output["choices"][0]["text"]), indent=4))  # type: ignore


def generate_create_vacancy_data(text: str):
    model_path = hf_hub_download(
        repo_id=config["local"]["repo_id"],
        filename=config["local"]["model"],
    )

    llm = Llama(
        model_path=model_path,
        n_ctx=config["local"]["n_ctx"],
        n_gpu_layers=-1,
        offload_kqv=True,
        verbose=True,
        n_threads=2,
    )
    question = f"""\
    You assume the role of an expert human resources manager. You are tasked to extract job details from a job posting. Avoid summarization and provide unchanged facts from the job posting.\n
    Here is the job posting:\n
    {text}
    """

    output = llm(
        question,
        grammar=LlamaGrammar.from_string(
            json_schema_to_grammar(json_schema_with_inlining(CreateVacancy), "")
        ),
        max_tokens=config["local"]["max_tokens"],
        temperature=config["local"]["temperature"],
    )

    print(json.dumps(json.loads(output["choices"][0]["text"]), indent=4))  # type: ignore
    return json.loads(output["choices"][0]["text"])


def generate_candidate_data(text):
    model_path = hf_hub_download(
        repo_id=config["local"]["repo_id"],
        filename=config["local"]["model"],
    )
    llm = Llama(
        model_path=model_path,
        n_ctx=config["local"]["n_ctx"],
        n_gpu_layers=-1,
        offload_kqv=True,
        verbose=True,
        n_threads=2,
    )
    question = f"""\
    You assume the role of an expert human resources manager. You are tasked to extract relevant information from candidate's resume.
    Preserve original text from responsibilities. Do not summarize, shorten or change original text.  
    Here's the candidate resume:\n
    {text}\
    """
    print(question)
    output = llm(
        question,
        grammar=LlamaGrammar.from_string(
            json_schema_to_grammar(json_schema_with_inlining(Candidate), "")
        ),
        max_tokens=config["local"]["max_tokens"],
        temperature=config["local"]["temperature"],
    )

    print(json.dumps(json.loads(output["choices"][0]["text"]), indent=4))  # type: ignore
    return json.loads(output["choices"][0]["text"])
