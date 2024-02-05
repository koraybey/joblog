import json

import tiktoken
import yaml
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.callbacks import CallbackManager, TokenCountingHandler
from llama_index.embeddings import HuggingFaceEmbedding, OpenAIEmbedding
from llama_index.llms import LlamaCPP, OpenAI
from llama_index.llms.llama_utils import (
    completion_to_prompt,
    messages_to_prompt,
)
from llama_index.readers import JSONReader

from models import Evaluation

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

with open("../static/candidate.json", "r") as file:
    candidate = json.load(file)


def evaluate_local():
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

    vacancy_data = JSONReader(input_files=["../static/vacancy.json"])

    vacancy_index = VectorStoreIndex.from_documents(
        vacancy_data,
        service_context=service_context,
    )

    query_engine = vacancy_index.as_query_engine(
        output_cls=Evaluation, refine_mode="compact"
    )

    def evaluation(responsibility: str):
        query = f"""\
        You are an expert human resources manager. You will be given a single line of text reflecting candidate's past experience. You must compare it against the job responsibilities and requirements, then provide an analysis.\n
        Your analysis must contain following details:
        original_text: Original text reflecting candidate's past experience.
        is_match: Does original text match the job responsibilities and requirements?
        is_relevant: Is original text relevant to job responsibilities and requirements?
        relevance_or_match_reason: Explain which job responsibilities or requirement matches or relates to the original text. Skip this text if there is neither relevance nor match between original text and job responsibilities or requirements. If there is a match or relevance, explain which job responsibilities or requirements original text relates to.
        improved_text: If original text is found to be a match or relevant, rewrite it to better align with the job requirements, responsibilities, writing style and most frequent keywords. Write in active language wherever appropriate and do not provide an explanation.\n
        Text from one of candidate's past experiences: {responsibility}\
        """
        response = query_engine.query(query)

        return response

    for candidate_experience in candidate["experience"]:
        for candidate_role_responsibility in candidate_experience[
            "candidate_role_responsibilities"
        ]:
            output = evaluation(
                candidate_role_responsibility, "Senior Product Manager at kevin."
            )
            print(output)


def evaluate_chat_local():
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

    vacancy_data = JSONReader(input_files=["../static/vacancy.json"])

    vacancy_index = VectorStoreIndex.from_documents(
        vacancy_data,
        service_context=service_context,
    )

    query_engine = vacancy_index.as_query_engine(
        output_cls=Evaluation, refine_mode="compact"
    )

    def evaluation(responsibility: str):
        query = f"""\
        You are an expert human resources manager. You will be given a single line of text reflecting candidate's past experience. You must compare it against the job responsibilities and requirements, then provide an analysis.\n
        Your analysis must contain following details:
        original_text: Original text reflecting candidate's past experience.
        is_match: Does original text match the job responsibilities and requirements?
        is_relevant: Is original text relevant to job responsibilities and requirements?
        relevance_or_match_reason: Explain which job responsibilities or requirement matches or relates to the original text. Skip this text if there is neither relevance nor match between original text and job responsibilities or requirements. If there is a match or relevance, explain which job responsibilities or requirements original text relates to.
        improved_text: If original text is found to be a match or relevant, rewrite it to better align with the job requirements, responsibilities, writing style and most frequent keywords. Write in active language wherever appropriate and do not provide an explanation.\n
        Text from one of candidate's past experiences: {responsibility}\
        """
        response = query_engine.query(query)

        return response

    for candidate_experience in candidate["experience"]:
        for candidate_role_responsibility in candidate_experience[
            "candidate_role_responsibilities"
        ]:
            output = evaluation(
                candidate_role_responsibility, "Senior Product Manager at kevin."
            )
            print(output)


def evaluate_openai():
    OpenAI.api_key = config["openai"]["api_key"]
    embed_model = OpenAIEmbedding(model_name=config["openai"]["embed_model"])
    token_counter = TokenCountingHandler(
        tokenizer=tiktoken.encoding_for_model(config["openai"]["model"]).encode
    )

    callback_manager = CallbackManager([token_counter])

    llm = OpenAI(
        model=config["openai"]["model"],
        temperature=config["openai"]["temperature"],
    )

    service_context = ServiceContext.from_defaults(
        llm=llm, embed_model=embed_model, callback_manager=callback_manager
    )

    vacancy_data = SimpleDirectoryReader(
        input_files=["../static/vacancy.json"]
    ).load_data()

    vacancy_index = VectorStoreIndex.from_documents(
        vacancy_data,
        service_context=service_context,
        llm=llm,
    )

    query_engine = vacancy_index.as_query_engine(
        output_cls=Evaluation, response_mode="compact"
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
        text from one of candidate's past experiences: {responsibility}\
        """
        response = query_engine.query(query)

        return response

    token_counter.reset_counts()

    for experience in candidate["experience"]:
        for responsibility in experience["responsibilities"]:
            output = evaluation(responsibility, "Senior Product Manager at kevin.")
            print(output)
            print(
                "Embedding Tokens: ",
                token_counter.total_embedding_token_count,
                "\n",
                "LLM Prompt Tokens: ",
                token_counter.prompt_llm_token_count,
                "\n",
                "LLM Completion Tokens: ",
                token_counter.completion_llm_token_count,
                "\n",
                "Total LLM Token Count: ",
                token_counter.total_llm_token_count,
                "\n",
            )
