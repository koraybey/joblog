#!make
include .env

PORT = 9999

serve: 
ifeq ($(MODEL_BACKEND),llamacpp)
	lmql serve-model llama.cpp:${MODEL_PATH} --port ${PORT} --n_gpu_layers -1 --n_ctx 4096
else ifeq ($(MODEL_BACKEND),transformers)
	lmql serve-model ${MODEL_PATH} --port ${PORT} --trust_remote_code True
else
	echo "MODEL_BACKEND is not set in .env. Currently, transformers and llama.cpp backends are supported."
endif
