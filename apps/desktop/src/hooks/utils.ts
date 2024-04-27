/* eslint-disable @typescript-eslint/no-unsafe-return */
import axios from 'axios'
import * as R from 'ramda'

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
            return new Error(`Things exploded: ${error}`)
        })

export const openUrl = (url: string) => () => void window.open(url)
export const copyToClipboard = (url: string) => () =>
    void navigator.clipboard.writeText(url)
