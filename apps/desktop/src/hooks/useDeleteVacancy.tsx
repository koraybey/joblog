import axios from 'axios'
import { mutate } from 'swr'

import { Vacancy } from '@/__generated__/gql/graphql'

import { allVacanciesQuery } from './useVacancy'

export const deleteVacancy = async ({ uid }: Pick<Vacancy, 'uid'>) =>
    await axios
        .post(
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
        .then(async (res) => {
            await mutate(allVacanciesQuery)
            return res
        })
        .catch((error) => {
            return new Error(`Things exploded: ${error}`)
        })
