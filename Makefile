ROOT_DIR := $(shell pwd)

all: api database frontend deployment

api:
    cd $(ROOT_DIR)/api && make

database:
    cd $(ROOT_DIR)/database && make

frontend:
    cd $(ROOT_DIR)/frontend && make

deployment:
    cd $(ROOT_DIR)/api && make
