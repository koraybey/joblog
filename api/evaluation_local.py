from typing import Optional
import yaml
import json
from pydantic import BaseModel
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)


class Evaluation(BaseModel):
    """Data model for candidate evaluation dimensions."""

    is_match: bool = False
    is_relevant: bool = False
    original_text: str = None
    relevance_or_match_reason: Optional[str] = None
    improved_text: Optional[str] = None


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

with open("../static/candidate.json", "r") as file:
    candidate = json.load(file)

embed_model = HuggingFaceEmbedding(model_name=config["local"]["embed_model"])

llm = LlamaCPP(
    model_path=f"model/{config['local']['model']}",
    context_window=config["local"]["n_ctx"],
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": -1},
    # transform inputs into Llama2 format
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)

service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

vacancy_data = SimpleDirectoryReader(input_files=["../static/vacancy.json"]).load_data()

vacancy_index = VectorStoreIndex.from_documents(
    vacancy_data,
    service_context=service_context,
)

query_engine = vacancy_index.as_query_engine(
    output_cls=Evaluation, refine_mode="compact"
)


def evaluation(responsibility: str, vacancy: str):
    query = f"""\
    You are an expert human resources manager, helping candidates get an interview by improving their resume to match the job requirements and responsibilities provided with the context.
    You will achieve your goal by comparing an text from one of candidate's past experiences against the job description and provide an analysis.\n
    Here is the analysis framework you must strictly apply:\n
    original_text: Original, unchanged text from one of candidate's past experiences.
    is_match: Determine if the text matches the job requirements and responsibilities provided with the context.
    is_relevant: Determine if the text is relevant to the job requirements and responsibilities.
    relevance_or_match_reason: Provide a brief explanation about relevance or match to the the job requirements and responsibilities. Quote original job requirement or responsibility if applicable.
    improved_text: If original text is relevant, rewrite it to better align with the job requirements, responsibilities, writing style and most frequent keywords. Write in active language wherever appropriate and do not provide an explanation.\n
    Role and company: {vacancy}
    Text from one of candidate's past experiences: {responsibility}\
    """
    response = query_engine.query(query)

    return response


for experience in candidate["experience"]:
    for responsibility in experience["responsibilities"]:
        output = evaluation(responsibility, "Senior Product Manager at kevin.")
        print(output)
