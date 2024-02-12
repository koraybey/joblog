from typing import Any

from gql import gql

from gql_.client_ import gql_client
from models import CreateVacancy


def create_vacancy_mutation(input_data: CreateVacancy) -> dict[str, Any]:
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
    return gql_client.execute(query, variable_values={"input": input_data})
