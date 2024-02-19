
# About 

This package exist, because SkyPilot dependencies conflict with api package dependencies. 

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


Install LambaCloud and RunPod dependencies by following the [documentation](https://skypilot.readthedocs.io/en/latest/getting-started/installation.html#lambda-cloud).

# Known issues


- Ports for the model server must be exposed manually. SkyPilot does not support opening ports on Runpod and Lambda via CLI.
- [If your cluster runs on non-x86_64 architecture (e.g., Apple Silicon), your image must be built natively for that architecture. Otherwise, your job may get stuck at Start streaming logs.](https://github.com/skypilot-org/skypilot/issues/3035)
