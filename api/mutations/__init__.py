from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="http://127.0.0.1:4000/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)


def create_vacancy_mutation(input_data):
    query = gql(
        """
        mutation CreateVacancy($input: VacancyInput!) {
            createVacancy(input: $input) {
                company
                position
                location
                contract
                remote
                salaryMin
                salaryMax
                about
                requirements
                responsibilities
            }
        }
    """
    )
    return client.execute(query, variable_values={"input": input_data})
