import importlib.resources

import yaml

config = yaml.safe_load(open(importlib.resources.path("config", "config.yaml"), "r"))
secret = yaml.safe_load(open(importlib.resources.path("config", "secrets.yaml"), "r"))
