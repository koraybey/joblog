/* eslint-disable @typescript-eslint/no-unsafe-return */
import axios from 'axios'
import * as R from 'ramda'
import useSWR from 'swr'

import { ThemeProvider } from '@/components/theme-provider'

import type { Vacancy } from './__generated__/gql/graphql'
import { columns } from './jobs/columns'
import { DataTable } from './jobs/data-table'

export const fetcher = (query: string) =>
    axios({
        url: 'http://127.0.0.1:4000/graphql',
        method: 'post',
        headers: { 'Content-type': 'application/json' },
        data: { query },
    })
        .then((res) => {
            return R.prop('data', res.data)
        })
        .catch((error) => {
            return new TypeError(`Things exploded: ${error}`)
        })

const App = () => {
    const { data, isLoading } = useSWR<{ allVacancies: Vacancy[] }>(
        `{
			allVacancies {
					uid
					companyLogo
					# description
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
			 }
		}
		`,
        fetcher
    )
    if (!data || isLoading) return

    return (
        <ThemeProvider defaultTheme={'dark'} storageKey={'vite-ui-theme'}>
            <DataTable columns={columns} data={data?.allVacancies} />
        </ThemeProvider>
    )
}

export default App
