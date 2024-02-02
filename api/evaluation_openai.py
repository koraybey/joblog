import yaml
import json
import tiktoken

from typing import Optional
from pydantic import BaseModel
from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAI
from llama_index.callbacks import CallbackManager, TokenCountingHandler


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

vacancy_data = SimpleDirectoryReader(input_files=["../static/vacancy.json"]).load_data()

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
