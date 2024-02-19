import subprocess

from paths import LOCAL_MODELS_FOLDER
from utils import load_config

config = load_config("models")

BACKEND = config["server"]["backend"]
MODEL = config["server"]["model"]
HOST = config["server"]["host"]
PORT = config["server"]["port"]
REPO_ID = config["server"]["repo_id"]

if BACKEND == "llamacpp":
    command = [
        f"lmql serve-model llama.cpp:{LOCAL_MODELS_FOLDER.absolute()}/{MODEL} --host {HOST} --port {PORT}\
                --n_gpu_layers -1 --n_ctx 4096"
    ]
else:
    command = [f"lmql serve-model {REPO_ID} --cuda --host {HOST} --port {PORT} --trust_remote_code True"]

subprocess.run(command, shell=True)
