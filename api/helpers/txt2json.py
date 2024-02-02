from llama_cpp.llama import Llama
from llama_cpp.llama_grammar import LlamaGrammar
from helpers.schema2grammar import schema2grammar
import json
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

llm = Llama(
    f"model/{config['local']['model']}",
    n_ctx=config["local"]["n_ctx"],
    n_gpu_layers=-1,
)


def txt2json(query, grammar):
    instructions = """
    Summarize the details and provide the result in JSON.
    Keep it brief and concise.
    """
    with open(grammar) as json_file:
        json_data = json.load(json_file)
    concatenated_query = instructions + "\n" + query
    print(concatenated_query)
    output = llm(
        concatenated_query,
        grammar=LlamaGrammar.from_string(schema2grammar(json_data, "")),
        max_tokens=config["local"]["max_tokens"],
        temperature=config["local"]["temperature"],
    )
    # print(json.dumps(json.loads(output['choices'][0]['text']), indent=4))
    return json.loads(output["choices"][0]["text"])  # type: ignore
