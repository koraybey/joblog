import axios from 'axios'
import { mutate } from 'swr'

import { Vacancy } from '@/__generated__/gql/graphql'

import { allVacanciesQuery } from './useVacancy'

export const updateVacancyQuery = `
mutation updateVacancy($input: VacancyMutation!) {
    updateVacancy(input: $input) { 
        uid
        status
    }
  }
`

export const updateVacancy = async ({
    uid,
    status,
}: Pick<Vacancy, 'uid' | 'status'>) =>
    await axios
        .post(
            'http://127.0.0.1:4000/graphql',
            {
                query: updateVacancyQuery,
                variables: {
                    input: {
                        uid,
                        status,
                    },
                },
            },
            {
                headers: { 'Content-type': 'application/json; charset=UTF-8' },
            }
        )
        .then(async (res) => {
            await mutate(allVacanciesQuery)
            return res
        })
        .catch((error) => {
            return new Error(`Things exploded: ${error}`)
        })
