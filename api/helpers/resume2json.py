from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding

import yaml
from pydantic import BaseModel, Field
from typing import List, Optional


class Experience(BaseModel):
    """Extraction model of the resume experience list."""

    company: str = Field(..., title="Company name")
    dateStart: str = Field(..., title="Date start")
    dateEnd: Optional[str] = Field(None, title="Date end")
    responsibilities: List[str] = Field(..., title="List of responsibilities")


class Resume(BaseModel):
    """Extraction model of the resume data."""

    id: str = Field(..., title="Person ID")
    name: str = Field(..., title="Name")
    location: str = Field(..., title="Location")
    about: Optional[str] = Field(None, title="About the person")
    experience: List[Experience] = Field(..., title="List of experiences")


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


embed_model = OpenAIEmbedding(model_name=config["openai"]["embed_model"])

OpenAI.api_key = f"model/{config['openai']['api_key']}"

llm = OpenAI(
    model=config["openai"]["model"],
    temperature=config["openai"]["temperature"],
    max_tokens=config["openai"]["max_tokens"],
)
service_context = ServiceContext.from_defaults(llm=llm)
documents = SimpleDirectoryReader("../static").load_data()
index = VectorStoreIndex.from_documents(
    documents, service_context=service_context, embed_model=embed_model
)

query_engine = index.as_query_engine(response_mode="compact", output_cls=Resume)

query_str = """
Extract candidate's resume and do not make any changes besides the structure to fit the data to the model provided. 
"""

response = query_engine.query(query_str)
print(response)
