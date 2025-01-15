
from gql import gql

from .gql_client import gql_client


def get_vacancy(uid: str) -> dict[str,str]:
    query = gql(
        """
        query GetVacancy($uid: String!) {
            getVacancy(uid: $uid){
                # company
                # title
                description
                # experienceLevel
                # contractType
                # workplaceType
                # location
            }
        }
        """
    )
    return gql_client.execute(query, variable_values={"uid": uid})
