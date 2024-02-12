# Installation (Unix/macOS)

Create a virtual environment

```shell
python3 -m venv .venv
```

Activate the environment

```shell
# zsh, bash
source .venv/bin/activate
# fish
source .venv/bin/activate.fish
```

Confirm virtual environment is active

```shell
which python
```

Install dependencies

```shell
pip install -r requirements.txt
```

Install stubs

```shell
mypy --install-types
```
