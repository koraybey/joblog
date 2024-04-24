ROOT_DIR := $(shell pwd)
CARGO = cargo

all: api database

api:
	packages/api/.venv/bin/python packages/api/main.py

database:
	cargo run database

check:
	$(CARGO) clippy

fmt:
	$(CARGO) fmt
