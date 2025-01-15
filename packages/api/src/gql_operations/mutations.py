import json

import humps
from gql import gql

from .gql_client import gql_client
from models import LinkedInJobPost


def create_vacancy(input_data: LinkedInJobPost) -> dict[str, str]:
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


def delete_vacancy(uid: str) -> dict[str, str]:
    query = gql(
        """
        mutation DeleteVacancy($uid: String!) {
			deleteVacancy(uid: $uid)
		}
        """
    )
    return gql_client.execute(query, variable_values={"uid": uid})
