import axios from 'axios'

import { Vacancy } from '@/__generated__/gql/graphql'

export const deleteVacancy = async ({ uid }: Pick<Vacancy, 'uid'>) =>
    await axios.post(
        'http://127.0.0.1:4000/graphql',
        {
            query: `
            mutation DeleteVacancy($uid: String!) {
                deleteVacancy(uid: $uid)
            }
            `,
            variables: { uid },
        },
        {
            headers: {
                'Content-Type': 'application/json',
            },
        }
    )
