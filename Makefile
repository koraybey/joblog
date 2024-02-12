ROOT_DIR := $(shell pwd)

all: api database frontend

api:
    cd $(ROOT_DIR)/database && make

database:
    cd $(ROOT_DIR)/frontend && make

frontend:
    cd $(ROOT_DIR)/api && make
