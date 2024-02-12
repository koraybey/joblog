import json

from huggingface_hub import hf_hub_download
from llama_cpp import Llama, LlamaGrammar

from models import Candidate, CreateVacancy, JobPosting
from utils import json_schema_to_grammar, json_schema_with_inlining, load_config

config = load_config("models")

model_path = hf_hub_download(
    repo_id=config["local_1"]["repo_id"],
    filename=config["local_1"]["model"],
    local_dir="local_models",
)

def generate_job_posting_data(text: str) -> JobPosting:
    question = f"""\
    You assume the role of an expert human resources manager. You are tasked to extract job details from a job posting. Avoid summarization and provide unchanged facts from the job posting.\n
    Here is the job posting:\n
    {text}
    """

    llm = Llama(
        model_path=model_path,
        n_ctx=config["local_1"]["n_ctx"],
        n_gpu_layers=-1,
        offload_kqv=True,
        verbose=True,
    )

    print(question)

    output = llm(
        question,
        grammar=LlamaGrammar.from_string(json_schema_to_grammar(json_schema_with_inlining(JobPosting))),
        max_tokens=config["local_1"]["max_tokens"],
        temperature=config["local_1"]["temperature"],
    )

    print(json.dumps(json.loads(output["choices"][0]["text"]), indent=4))  # type: ignore[index]
    json_output: JobPosting = json.loads(output["choices"][0]["text"])  # type: ignore[index]
    return json_output


def generate_create_vacancy_data(text: str) -> CreateVacancy:
    question = f"""\
    You assume the role of an expert human resources manager. You are tasked to extract job details from a job posting. Avoid summarization and provide unchanged facts from the job posting.\n
    Here is the job posting:\n
    {text}
    """

    llm = Llama(
        model_path=model_path,
        n_ctx=config["local_1"]["n_ctx"],
        n_gpu_layers=-1,
        offload_kqv=True,
        verbose=True,
    )

    print(question)

    output = llm(
        question,
        grammar=LlamaGrammar.from_string(json_schema_to_grammar(json_schema_with_inlining(CreateVacancy))),
        max_tokens=config["local_1"]["max_tokens"],
        temperature=config["local_1"]["temperature"],
    )

    print(json.dumps(json.loads(output["choices"][0]["text"]), indent=4))  # type: ignore[index]
    json_output: CreateVacancy = json.loads(output["choices"][0]["text"])  # type: ignore[index]
    return json_output


def generate_candidate_data(text: str) -> Candidate:
    question = f"""\
    You assume the role of an expert human resources manager. \
    You are tasked to extract relevant information from candidate's resume.
    Preserve original text from responsibilities. Do not summarize, shorten or change original text.
    Do not add any additional information that is not on the resume.
    Here's the candidate resume:\n
    {text}\
    """

    llm = Llama(
        model_path=model_path,
        n_ctx=config["local_1"]["n_ctx"],
        n_gpu_layers=-1,
        offload_kqv=True,
        verbose=True,
    )

    print(question)

    output = llm(
        question,
        grammar=LlamaGrammar.from_string(json_schema_to_grammar(json_schema_with_inlining(Candidate))),
        max_tokens=config["local_1"]["max_tokens"],
        temperature=config["local_1"]["temperature"],
    )

    print(json.dumps(json.loads(output["choices"][0]["text"]), indent=4))  # type: ignore[index]
    json_output: Candidate = json.loads(output["choices"][0]["text"])  # type: ignore[index]
    return json_output
