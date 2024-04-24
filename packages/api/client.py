import os

from dotenv import load_dotenv
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from exceptions import UnconfiguredEnvironmentError

load_dotenv()

GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT")

if GRAPHQL_ENDPOINT is None:
    raise UnconfiguredEnvironmentError

_transport = AIOHTTPTransport(url=GRAPHQL_ENDPOINT)
gql_client = Client(transport=_transport, fetch_schema_from_transport=True)
