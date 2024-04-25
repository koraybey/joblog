ROOT_DIR := $(shell pwd)
CARGO = cargo

all: api database desktop

desktop:
	cd apps/desktop && bun run tauri dev

api:
	packages/api/.venv/bin/python packages/api/main.py

database:
	cargo run --bin database

check:
	$(CARGO) clippy

fmt:
	$(CARGO) fmt
