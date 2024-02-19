# Installation

This module uses [uv package manager.](https://github.com/astral-sh/uv). You must install it first to create a venv and install the dependencies.

Create a virtual environment

```shell
uv venv  # Create a virtual environment at .venv
```

Activate the environment

```shell
# zsh, bash
source .venv/bin/activate
# fish
source .venv/bin/activate.fish
# windows
.\.venv\Scripts\activate.ps1
```

Confirm virtual environment is active

```shell
which python
```

Install dependencies

```shell
uv pip install -r requirements.txt  # Install from a requirements.txt file.
```

Install stubs

```shell
mypy --install-types
```
