
# About 

This package exist, because SkyPilot dependencies conflict with api package dependencies. 

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

Install LambaCloud and RunPod dependencies by following the [documentation](https://skypilot.readthedocs.io/en/latest/getting-started/installation.html#lambda-cloud).

# Known issues


- [If your cluster runs on non-x86_64 architecture (e.g., Apple Silicon), your image must be built natively for that architecture. Otherwise, your job may get stuck at Start streaming logs.](https://github.com/skypilot-org/skypilot/issues/3035)
