/* eslint-disable @typescript-eslint/no-unsafe-return */
import axios from 'axios'
import * as R from 'ramda'
import useSWR from 'swr'

import { Vacancy } from '@/__generated__/gql/graphql'

export const allVacanciesQuery = `
{
    allVacancies {
        uid
        companyLogo
        description
        company
        title
        experienceLevel
        contractType
        workplaceType
        location
        url
        companyUrl
        dateCreated
        dateModified
        status
    }
}
`

export const fetcher = (query: string) =>
    axios({
        url: 'http://127.0.0.1:4000/graphql',
        method: 'post',
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        data: { query },
    })
        .then((res) => {
            return R.prop('data', res.data)
        })
        .catch((error) => {
            return new TypeError(`Things exploded: ${error}`)
        })

export const useVacancy = () => {
    return useSWR<{ allVacancies: Vacancy[] }>(allVacanciesQuery, fetcher)
}
