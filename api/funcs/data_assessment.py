from typing import Any

import chromadb
import lmql
from huggingface_hub import hf_hub_download
from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.core.base_query_engine import BaseQueryEngine
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import (
    completion_to_prompt,
    messages_to_prompt,
)
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import ChromaVectorStore
from lmql import LLM

from paths import DATABASE_DIR, LOCAL_MODELS_FOLDER, STATIC_FOLDER
from utils import load_config

config = load_config("models")

LOCAL_MODEL_NAME = config["local"]["model"]
LOCAL_MODEL_TOKENIZER = config["local"]["tokenizer"]
ABS_LOCAL_MODEL_PATH = f"{LOCAL_MODELS_FOLDER}/{LOCAL_MODEL_NAME}"


def _load_model(): # type: ignore[return,empty-body, no-untyped-def]
    vect_model_path = hf_hub_download(
        repo_id=config["local"]["repo_id"],
        filename=config["local"]["model"],
        local_dir="local_models",
    )

    lmql_model = lmql.model(
        f"local:llama.cpp:{ABS_LOCAL_MODEL_PATH}", tokenizer=LOCAL_MODEL_TOKENIZER, n_gpu_layers=-1, n_ctx=4096
    )
    embed_model = HuggingFaceEmbedding(model_name=config["local"]["embed_model"])

    llm = LlamaCPP(
        model_path=vect_model_path,
        context_window=config["local"]["n_ctx"],
        model_kwargs={"n_gpu_layers": -1, "n_ctx": 4096},
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=True,
    )

    database = chromadb.PersistentClient(path=str(DATABASE_DIR))
    chroma_collection = database.get_or_create_collection("jobs")

    job_service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )

    job_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    job_storage_context = StorageContext.from_defaults(vector_store=job_vector_store)

    job_data = SimpleDirectoryReader(str(STATIC_FOLDER / "jobs")).load_data()

    job_index = VectorStoreIndex.from_documents(
        job_data, storage_context=job_storage_context, service_context=job_service_context
    )

    jobs_query_engine = job_index.as_query_engine(response_mode="no_text", similarity_top_k=1)

    return lmql_model, jobs_query_engine


@lmql.query()
def _analyse_resume_bullet_query(resume_bullet, lmql_model, jobs_query_engine):  # type: ignore[return,empty-body, no-untyped-def]
    # fmt: off
    '''lmql
    argmax
        "You assume the role of an expert human resources manager, hiring the best talent for the role."
        "You will be given a resume bullet from candidate's resume for assessment."
        "You must compare it against the job responsibilities and requirements."

        "Resume bullet: {resume_bullet}"

        job_description_query = jobs_query_engine.query(resume_bullet)
        job_description = "\n\n".join([s.node.get_text() for s in job_description_query.source_nodes])
        "Job requirements and responsibilities: {job_description}"

        "Is resume bullet relevant to job requirements and responsibilities?:[BOOL_RELEVANCE]\n"
        "Does resume bullet match job requirements and responsibilities?:[BOOL_MATCH]\n"
        "Briefly explain the relevance or match reason:[STRING_EXPLANATION]\n"
    from lmql_model
    where
    STOPS_AT(STRING_EXPLANATION, "\n") and len(TOKENS(STRING_EXPLANATION)) < 150
     and BOOL_RELEVANCE in ["true", "false"] and BOOL_MATCH in ["true", "false"]
    '''
    # fmt: on


@lmql.query()
def _create_example_resume_bullet(resume_bullet, lmql_model, jobs_query_engine):  # type: ignore[return,empty-body, no-untyped-def]
    # fmt: off
    '''lmql
    argmax
        "You assume the role of an expert human resources manager, hiring the best talent for the role."
        "You will be given a resume bullet from candidate's resume for assessment."

        "Resume bullet: {resume_bullet}"

        job_description_query = jobs_query_engine.query(resume_bullet)
        job_description = "\n\n".join([s.node.get_text() for s in job_description_query.source_nodes])
        "Job requirements and responsibilities: {job_description}"

        "Create an example bullet point from original, tailored to the job requirements and responsibilities."

        "Example bullet point:•[STRING_EXAMPLE]\n"
    from lmql_model
    where
        STOPS_AT(STRING_EXAMPLE, ".") and len(TOKENS(STRING_EXAMPLE)) < 150
    '''
    # fmt: on


def analyse_resume_bullet(resume_bullet: str) -> dict[str, Any]:
    lmql_model, jobs_query_engine  = _load_model()
    result = _analyse_resume_bullet_query(resume_bullet, lmql_model, jobs_query_engine)
    json_result = {
        "is_match": result.variables["BOOL_MATCH"],
        "is_relevant": result.variables["BOOL_RELEVANCE"],
        "relevance_or_match_reason": result.variables["STRING_EXPLANATION"].strip(),
    }
    return json_result


def create_example_resume_bullet(resume_bullet: str) -> Any:
    lmql_model, jobs_query_engine  = _load_model()
    result = _create_example_resume_bullet(resume_bullet, lmql_model, jobs_query_engine)
    return result.variables["STRING_EXAMPLE"].strip()
