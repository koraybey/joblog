import yaml
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from llama_index import SQLDatabase
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from sqlalchemy import create_engine

with open("../config.yaml", "r") as file:
    config = yaml.safe_load(file)

engine = create_engine("postgresql+psycopg2://koraybey@localhost:5432/joblog")

model_path = hf_hub_download(
    repo_id=config["local"]["repo_id"],
    filename=config["local"]["model"],
)

llm = Llama(
    model_path=model_path,
    n_ctx=config["local"]["n_ctx"],
    n_gpu_layers=-1,
)

sql_database = SQLDatabase(engine, include_tables=["vacancies"])

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["vacancies"],
)

query_str = """Provide a breakdown of all vacancies."""
response = query_engine.query(query_str)
print(response)
