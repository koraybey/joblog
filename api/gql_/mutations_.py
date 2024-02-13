import json
from typing import Any

import humps
from gql import gql

from gql_.client_ import gql_client
from models import LinkedInJobPost


def create_vacancy_mutation(input_data: LinkedInJobPost) -> dict[str, Any]:
    query = gql(
        """
        mutation CreateVacancy($input: VacancyInput!) {
            createVacancy(input: $input) {
                companyLogo
                company
                title
                description
                experienceLevel
                contractType
                location
                workplaceType
                url
                companyUrl
            }
        }
    """
    )
    json_data = humps.camelize(json.loads(input_data.model_dump_json()))
    return gql_client.execute(query, variable_values={"input": json_data})


def delete_vacancy_mutation(uid: str) -> dict[str, Any]:
    query = gql(
        """
        mutation DeleteVacancy($id: String!) {
            deleteVacancy(id: $id)
        }
     """
    )
    return gql_client.execute(query, variable_values={"id": uid})
