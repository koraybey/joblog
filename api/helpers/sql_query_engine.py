import yaml

from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index import SQLDatabase, ServiceContext
from llama_index.llms import OpenAI
from sqlalchemy import create_engine

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

engine = create_engine("postgresql+psycopg2://koraybey@localhost:5432/joblog")
OpenAI.api_key = OpenAI.api_key = f"model/{config['openai']['api_key']}"

llm = OpenAI(model="gpt-4-1106-preview", temperature=0.1)
service_context = ServiceContext.from_defaults(llm=llm)
sql_database = SQLDatabase(engine, include_tables=["vacancies"])

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["vacancies"],
)

query_str = """Provide a breakdown of all vacancies."""
response = query_engine.query(query_str)
print(response)
