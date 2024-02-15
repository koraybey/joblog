from typing import Any

from gql import gql

from gql_.client_ import gql_client


def query_get_vacancy(uid: str) -> dict[str, Any]:
    query = gql(
        """
        query GetVacancy($uid: String!) {
            getVacancy(uid: $uid){
                company
                title
                description
                experienceLevel
                contractType
                workplaceType
                location
            }
        }
     """
    )
    return gql_client.execute(query, variable_values={"uid": uid})
