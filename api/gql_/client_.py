import os

from dotenv import load_dotenv
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport


# TODO Move custom exceptions somewhere else.
class UnconfiguredEnvironmentError(Exception):
    """Base class for unconfigured environment."""
    pass

load_dotenv()

GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT")
if GRAPHQL_ENDPOINT is None:
    raise UnconfiguredEnvironmentError

_transport = AIOHTTPTransport(url=GRAPHQL_ENDPOINT)
gql_client = Client(transport=_transport, fetch_schema_from_transport=True)
