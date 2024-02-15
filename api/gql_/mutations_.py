import json
from typing import Any

import humps
from gql import gql

from gql_.client_ import gql_client
from models import LinkedInJobPost


def mutation_create_vacancy(input_data: LinkedInJobPost) -> dict[str, Any]:
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


def mutation_delete_vacancy(uid: str) -> dict[str, Any]:
    query = gql(
        """
        mutation DeleteVacancy($uid: String!) {
            deleteVacancy(uid: $uid)
        }
     """
    )
    return gql_client.execute(query, variable_values={"uid": uid})
